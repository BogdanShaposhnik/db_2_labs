from .ViewMenu import BaseViewerScreen
from chat.Message import Message
from chat import constants

NEXT = 'next'
PREV = 'prev'
BACK = 'back'


class ReadMessageScreen(BaseViewerScreen):
    def __init__(self, state):
        super().__init__(items_per_page=20)
        self.state = state
        self.redis = self.state['redis']
        self.selected_message = None

    def get_key(self):
        return '%s:%s' % (constants.INCOMING_MESSAGES_Z, self.state['user'].login)

    def fetch(self, start, end):
        return self.redis.zrange(self.get_key(), start, end)

    def items_count(self):
        return self.redis.zcard(self.get_key())

    def render(self):
        while True:
            self.clear()
            if self.selected_message:
                print(self.selected_message.pstr())
            choices = [PREV, NEXT, BACK]
            choices.extend(self.load())
            actions = {
                NEXT: self.next_page,
                PREV: self.prev_page,
                BACK: None
            }
            answers = self.ask([{
                'type': 'list',
                'name': 'item',
                'message': 'Navigation',
                'choices': choices
            }])
            if answers['item'] in actions:
                if answers['item'] == BACK:
                    return
                actions[answers['item']]()
                self.clear()
            else:
                # it contains id of selected message
                self.selected_message = Message.load(answers['item'], self.redis)
                self.selected_message.read(self.state['user'].login)
