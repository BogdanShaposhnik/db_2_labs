from .ChooseMenu import BaseScene
from .MainMenu import MenuScreen
from .WorkerMenu import WorkerScreen
from .User_Emulation import AutomatronScreen
from chat.User import User
from chat import constants

BE_WORKER = 'worker'
START_EMULATION = 'emulation'
BE_USER = 'user/admin'
EXIT = 'exit'


def login_validator(val):
    if not len(str(val).strip()):
        return 'Login cannot be empty'


PROMPT = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            BE_WORKER,
            BE_USER,
            START_EMULATION,
            EXIT
        ]
    },
    {
        'type': 'input',
        'name': 'login',
        'message': 'Your login (if it is start with "admin", you will have admin access)',
        'condition': lambda answers: answers['action'] == BE_USER,
        'validate': login_validator
    }
]


class StartScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.redis = state['redis']
        self.state = state
        self.thread = None

    def be_worker(self, *args):
        WorkerScreen(self.state).render()

    def subscribe(self, events_handlers):
        if self.thread:
            self.thread.stop()
        p = self.redis.pubsub()
        p.psubscribe(**events_handlers)
        self.thread = p.run_in_thread(sleep_time=0.001)

    def be_user(self, answers):
        login = str(answers['login']).strip()
        user = User.load(self.redis, login)
        is_admin = login.startswith('admin')
        if not user:
            user = User(login, 'admin' if is_admin else 'user', self.redis)
            user.save()
        self.state['user'] = user
        if is_admin:
            self.subscribe({
                # as user
                '%s:%s' % (constants.MESSAGE_CREATED_EVENT, login): self.handle_message_created,
                '%s:%s' % (constants.INCOMING_MESSAGE_EVENT, login): self.handle_incoming_message,
                '%s:%s' % (constants.MESSAGE_APPROVED_EVENT, login): self.handle_message_approve,
                '%s:%s' % (constants.MESSAGE_BLOCKED_EVENT, login): self.handle_message_block,
                '%s:%s' % (constants.MESSAGE_READ_EVENT, login): self.handle_message_read,
                # as admin
                '%s:*' % constants.MESSAGE_CREATED_EVENT: self.handle_else_message_created,
                '%s:*' % constants.INCOMING_MESSAGE_EVENT: self.handle_else_incoming_message,
                '%s:*' % constants.MESSAGE_APPROVED_EVENT: self.handle_else_message_approve,
                '%s:*' % constants.MESSAGE_BLOCKED_EVENT: self.handle_else_message_block,
                '%s:*' % constants.MESSAGE_READ_EVENT: self.handle_else_message_read,
            })
        else:
            self.subscribe({
                '%s:%s' % (constants.MESSAGE_CREATED_EVENT, login): self.handle_message_created,
                '%s:%s' % (constants.INCOMING_MESSAGE_EVENT, login): self.handle_incoming_message,
                '%s:%s' % (constants.MESSAGE_APPROVED_EVENT, login): self.handle_message_approve,
                '%s:%s' % (constants.MESSAGE_BLOCKED_EVENT, login): self.handle_message_block,
                '%s:%s' % (constants.MESSAGE_READ_EVENT, login): self.handle_message_read,
            })
        MenuScreen(self.state).render()

    @staticmethod
    def handle_else_message_read(msg):
        print(
            ' %s\'s message %s was read' % (msg['channel'].split(':')[-1], msg['data']))

    @staticmethod
    def handle_else_message_created(msg):
        print(' %s create a message %s' % (msg['channel'].split(':')[1], msg['data']))

    @staticmethod
    def handle_else_incoming_message(msg):
        print(' %s has an incoming message %s' % (msg['channel'].split(':')[1], msg['data']))

    @staticmethod
    def handle_else_message_approve(msg):
        print(' %s message %s was approved' % (msg['channel'].split(':')[1], msg['data']))

    @staticmethod
    def handle_else_message_block(msg):
        print(' %s message %s was blocked' % (msg['channel'].split(':')[1], msg['data']))

    @staticmethod
    def handle_message_created(msg):
        print('️ Your message %s created' % msg['data'])

    @staticmethod
    def handle_incoming_message(msg):
        print('️ You have a new incoming message: %s' % msg['data'])

    @staticmethod
    def handle_message_approve(msg):
        print('Your message %s was approved' % msg['data'])

    @staticmethod
    def handle_message_block(msg):
        print('️ Your message %s was blocked' % msg['data'])

    @staticmethod
    def handle_message_read(msg):
        print(' %s read your message %s' % (msg['channel'].split(':')[-1], msg['data']))

    def start_emulation(self, *args):
        AutomatronScreen(self.state).render()

    def render(self):
        actions = {
            BE_WORKER: self.be_worker,
            BE_USER: self.be_user,
            START_EMULATION: self.start_emulation
        }
        while True:
            if self.thread:
                self.thread.stop()
            answers = self.ask(PROMPT)
            if answers['action'] in actions:
                actions[answers['action']](answers)
                print("1")
            else:
                return
