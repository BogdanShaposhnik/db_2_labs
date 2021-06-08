from .ChooseMenu import BaseScene
from chat.Message import Message

APPROVE = 'approve'
BLOCK = 'block'
BACK = 'back'

PROMPT = [{
    'type': 'list',
    'message': 'Approve/block?',
    'name': 'action',
    'choices': [
        APPROVE,
        BLOCK
    ]
}]
CONTINUE_PROMPT = [{
    'type': 'accept',
    'message': 'Continue?',
    'name': 'action',
}]


class ModerationScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.redis = self.state['redis']

    @staticmethod
    def approve(message):
        message.approve()

    @staticmethod
    def block(message):
        message.block()

    def render(self):
        actions = {
            APPROVE: self.approve,
            BLOCK: self.block
        }
        while True:
            self.clear()
            message = Message.get_next_unprocessed(self.redis)
            if message:
                print(message.pstr())
                answers = self.ask(PROMPT)
                if answers['action'] in actions:
                    actions[answers['action']](message)
                self.clear()
            else:
                print('No new messages :(')
            answers = self.ask(CONTINUE_PROMPT)
            if not answers['action']:
                return
