from chat import constants
from datetime import datetime
import time
from chat.Neo4j import GraphDB


def now():
    return int(round(time.time() * 1000))


def str_now():
    return datetime.now().strftime('%Y-%m-%d-%H.%M.%S')


MESSAGES_GROUPS = [
    constants.WAIT_FOR_MODERATION_MESSAGES_Z,
    constants.READ_MESSAGES_Z,
    constants.APPROVED_MESSAGES_Z,
    constants.MESSAGES_ON_MODERATION_Z
]

db = GraphDB()


class Message:
    def __init__(self,
                 redis,
                 sender,
                 receiver,
                 text,
                 status=constants.STATUS_MESSAGE_CREATED,
                 **kwargs
                 ):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.status = status
        self.created_at = kwargs['created_at'] if 'created_at' in kwargs else now()
        self.id = kwargs['id'] if 'id' in kwargs else '%s:%s:%s' % (self.sender, self.receiver, str_now())
        self.redis = redis
    def to_dict(self):
        return {
            'text': self.text,
            'receiver': self.receiver,
            'sender': self.sender,
            'status': self.status,
            'id': self.id,
            'created_at': self.created_at
        }

    def pstr(self):
        return ('id     {id}\n'
                'from   {sender}\n'
                'to     {receiver}\n'
                'at     {created_at}\n'
                'status {status}\n'
                '------\n'
                '{text}\n'
                '------\n').format(**self.to_dict())

    def save(self):
        self.redis.hmset('%s:%s' % (constants.MESSAGES_STORAGE, self.id), self.to_dict())

    @staticmethod
    def load(mid, redis):
        saved_msg = redis.hgetall('%s:%s' % (constants.MESSAGES_STORAGE, mid))
        if not saved_msg:
            return None
        return Message(**saved_msg, redis=redis)

    def update_status(self, status, dest_group, pipeline=None):
        p = pipeline or self.redis.pipeline()
        for group in MESSAGES_GROUPS:
            p.zrem('%s:%s' % (group, self.sender), self.id)
        p.zadd('%s:%s' % (dest_group, self.sender), {self.id: now()})
        p.hset('%s:%s' % (constants.MESSAGES_STORAGE, self.id), 'status', status)
        if not pipeline:
            p.execute()

    def publish(self):
        p = self.redis.pipeline()
        # save message data
        self.save()
        # push event about created message
        p.publish('%s:%s' % (constants.MESSAGE_CREATED_EVENT, self.sender), self.id)
        # add message to list of unprocessed messages for workers
        p.sadd(constants.SET_WAIT_FOR_MODERATION, self.id)

        db.send_message(self.sender, self.receiver, self.text, constants.WAIT_FOR_MODERATION_MESSAGES_Z, self.id)

        # add message to list of sender's sent messages
        p.zadd('%s:%s' % (constants.SENT_MESSAGES_Z, self.sender), {self.id: now()})
        self.update_status(constants.STATUS_MESSAGE_CREATED, constants.WAIT_FOR_MODERATION_MESSAGES_Z)
        # save to action log
        p.lpush(constants.LIST_ACTION_LOGS, 'user "%s" send message "%s"' % (self.sender, self.id))
        p.execute()

    @staticmethod
    def get_next_unprocessed(redis):
        mid = redis.srandmember(constants.SET_WAIT_FOR_MODERATION, 1)
        if not mid or not mid[0]:
            return
        mid = mid[0]
        message = Message.load(mid, redis)
        p = redis.pipeline()
        # delete message from list of unprocessed messages
        p.srem(constants.SET_WAIT_FOR_MODERATION, mid)
        message.update_status(constants.STATUS_MESSAGE_ON_MODERATION, constants.MESSAGES_ON_MODERATION_Z)
        # write logs
        p.lpush(constants.LIST_ACTION_LOGS, 'admins took message "%s" on moderation' % mid)
        p.execute()
        return message

    def approve(self):
        p = self.redis.pipeline()
        # mark message as approved
        self.update_status(constants.STATUS_MESSAGE_APPROVED, constants.APPROVED_MESSAGES_Z)
        # append event to log
        p.lpush(constants.LIST_ACTION_LOGS, 'admin approve message "%s"' % self.id)
        # increase number of sent messages of the message author
        p.zincrby(constants.ACTIVE_SENDERS_Z, 1, self.sender)
        # add message to queue of incoming messages receiver
        p.zadd('%s:%s' % (constants.INCOMING_MESSAGES_Z, self.receiver), {self.id: self.created_at})
        # publish event, message approved to author
        p.publish('%s:%s' % (constants.MESSAGE_APPROVED_EVENT, self.sender), self.id)
        # publish event, incoming message to addresser
        p.publish('%s:%s' % (constants.INCOMING_MESSAGE_EVENT, self.receiver), self.id)

        db.update_message(constants.STATUS_MESSAGE_APPROVED, self.id)

        p.execute()

    def block(self):
        p = self.redis.pipeline()
        # mark message as spam
        self.update_status(constants.STATUS_MESSAGE_BLOCKED, constants.BLOCKED_MESSAGES_Z)
        # increase number of sent messages of the message author
        p.zincrby(constants.SPAMMERS_Z, 1, self.sender)
        # publish event, message approved to author
        p.publish('%s:%s' % (constants.MESSAGE_BLOCKED_EVENT, self.sender), self.id)
        # append event to log
        p.lpush(constants.LIST_ACTION_LOGS, 'admin block message "%s"' % self.id)

        db.update_message(constants.STATUS_MESSAGE_BLOCKED, self.id)

        p.execute()

    def read(self, by_who):
        p = self.redis.pipeline()
        self.update_status(constants.STATUS_MESSAGE_READ, constants.READ_MESSAGES_Z)
        # append event to log
        p.lpush(constants.LIST_ACTION_LOGS, 'user "%s" read message "%s"' % (by_who, self.id))
        # publish event, message approved to author
        p.publish('%s:%s' % (constants.MESSAGE_READ_EVENT, self.sender), self.id)
        p.execute()
