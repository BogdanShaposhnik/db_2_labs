from .BaseScreen import BaseScene
from chat import constants
from chat.Message import Message
from chat.User import User
from random import random
from multiprocessing import Queue
import math
import time
import multiprocessing.dummy
from multiprocessing import Manager
import lorem

USERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
TAGS = ['Hi', 'Hello', 'Bye', 'Hey', 'Goodbye']

def int_validator(val):
    try:
        if int(val) <= 0:
            return 'value should be greater than 0'
    except ValueError:
        return 'Value is not a valid integer'


PROMPT = [
    {
        'type': 'input',
        'validate': int_validator,
        'name': 'count',
        'message': 'Enter count of users'
    },
    {

        'type': 'input',
        'validate': int_validator,
        'name': 'delay',
        'message': 'Enter delay in sec between their actions'
    }
]


class AutomatronScreen(BaseScene):

    def __init__(self, state):
        super().__init__()
        self.redis = state['redis']
        self.state = state
        self.workers = []
        self.users = []

    def run(self, delay):

        self.workers = [multiprocessing.dummy.Process(target=self.work, args=(user, delay,)) for user in self.users]
        for w in self.workers:
            w.start()

    def work(self, user, delay):

        while True:
            time.sleep(random() * delay)
            time.sleep(random() * delay)
            if (random() < 0.3):
                print('👁 %s wants to read a message' % user.login)
                mid = self.redis.zpopmin('%s:%s' % (constants.INCOMING_MESSAGES_Z, user.login))
                if not mid or not mid[0]:
                    print('❗️But %s has not a new message' % user.login)
                    continue
                mid = mid[0][0]
                msg = Message.load(mid, self.redis)
                msg.read(user.login)
                print('👀 %s read a message %s' % (user.login, mid))
            else:
                receiver = self.logins[math.floor(random() * len(self.logins))]
                print('✏️ %s writes a message to %s' % (user.login, receiver))
                if random() < 0.2:
                    txt = TAGS[round(random()*4)]
                else:
                    txt = lorem.sentence()
                msg = Message(sender=user.login, receiver=receiver, text=txt, redis=self.redis)
                msg.publish()

    def stop(self):
        for p in self.workers:
            p.terminate()
        for p in self.workers:
            p.join()

    def render(self):
        answers = self.ask(PROMPT)
        count = int(answers['count'])
        delay = int(answers['delay'])
        self.logins = USERS[:count]
        self.users = [User(
            login=login,
            role='user',
            redis=self.redis
        ) for login in self.logins]
        print('Start auto chat  with this users: %s', '\n'.join(self.logins))
        print('press ⏎ to exit')
        self.run(delay)
        input()
        self.stop()
