from .ChooseMenu import BaseScene
from chat.User import User
from chat.Message import Message
import lorem


class MessageCreationScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.redis = self.state['redis']

    def send_message(self):
        pass

    def get_prompt(self):
        return [
            {
                'type': 'list',
                'name': 'receiver',
                'message': 'Who do you want to send a letter to?',
                'choices': User.get_all_users_logins(self.state['redis'])
            },
            {
                'type': 'input',
                'name': 'text',
                'message': 'Enter message text:',
                'default': lorem.sentence
            }
        ]

    def render(self):
        prompt = self.get_prompt()
        answers = self.ask(prompt)
        message = Message(
            sender=self.state['user'].login,
            text=answers['text'],
            receiver=answers['receiver'],
            redis=self.redis
        )
        message.publish()
