from .BaseScreen import BaseScene
from chat import constants
from chat.Message import Message
from random import random


class WorkerScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.redis = state['redis']
        self.state = state
        self.thread = None

    def subscribe(self, events_handlers):
        if self.thread:
            self.thread.stop()
        p = self.redis.pubsub()
        p.psubscribe(**events_handlers)
        self.thread = p.run_in_thread(sleep_time=0.001)

    def handle_message_created_event(self, message):
        self.moderate_message(Message.load(message['data'], self.redis))

    def process_old(self):
        while True:
            message = Message.get_next_unprocessed(self.redis)
            if not message:
                break
            self.moderate_message(message)

    @staticmethod
    def moderate_message(message):
        print('⚡️I received msg %s, working...' % message.id)
        if random() > 0.8:
            print('❤️ I blocked msg %s' % message.id)
            message.block()
        else:
            print('💚 I approved msg %s' % message.id)
            message.approve()

    def subscribe_to_events(self):
        self.subscribe({
            '%s:*' % constants.MESSAGE_CREATED_EVENT: self.handle_message_created_event
        })

    def render(self):
        print('wait, I\'m processing old messages')
        self.process_old()
        print('press ⏎ to exit')
        self.subscribe_to_events()
        input()
        self.thread.stop()
