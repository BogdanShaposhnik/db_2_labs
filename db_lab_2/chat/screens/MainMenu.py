from .ChooseMenu import BaseScene
from .MessageCreator import MessageCreationScreen
from chat.screens.lists.ListSentMessageScreen import ListSentScreen
from chat.screens.lists.ListCreatedMessagesScreen import ListCreatedScreen
from chat.screens.lists.ListModeratingMessageScreen import ListModeratingScreen
from chat.screens.lists.ListApprovedMessagesScreen import ListApprovedScreen
from chat.screens.lists.ListBlockedMessagesScreen import ListBlockedScreen
from chat.screens.lists.ListReadMessageScreen import ListReadScreen
from chat.screens.lists.ListIncomingMessagesScreen import ListIncomingMessagesScreen
from chat.screens.lists.ListActiveSendersScreen import ListActiveSendersScreen
from chat.screens.lists.ListActiveSpammersScreen import ListActiveSpammersScreen
from chat.screens.lists.ListActionLogsScreen import ListActionLogsScreen
from chat.screens.ModerationScreen import ModerationScreen
from chat.screens.ReadMessageScreen import ReadMessageScreen

SEND_A_MESSAGE = 'send a new message'
READ_MESSAGE = 'read message'
LIST_SENT_MESSAGES = 'list sent messages'
LIST_UNPROCESSED_MESSAGES = 'list unprocessed messages'
LIST_MESSAGES_ON_MODERATION = 'list messages, which are moderating now'
LIST_APPROVED_MESSAGES = 'list approved messages'
LIST_BLOCKED_MESSAGES = 'list blocked messages'
LIST_READ_MESSAGES = 'list delivered messages'
LIST_INCOMING_MESSAGES = 'list incoming messages'
MODERATE_MESSAGES = 'moderate messages'
LIST_ACTIVE_SPAMMERS = 'list of active spammers'
LIST_ACTIVE_SENDERS = 'list of active senders'
LIST_ACTIONS_LOGS = 'list actions logs'
BACK = 'back'

ADMIN_PROMPT = [
    {
        'type': 'list',
        'name': 'item',
        'message': 'What\'s next?',
        'choices': [
            SEND_A_MESSAGE,
            READ_MESSAGE,
            LIST_SENT_MESSAGES,
            LIST_UNPROCESSED_MESSAGES,
            LIST_MESSAGES_ON_MODERATION,
            LIST_APPROVED_MESSAGES,
            LIST_BLOCKED_MESSAGES,
            LIST_READ_MESSAGES,
            LIST_INCOMING_MESSAGES,
            MODERATE_MESSAGES,
            LIST_ACTIVE_SENDERS,
            LIST_ACTIVE_SPAMMERS,
            LIST_ACTIONS_LOGS,
            BACK
        ]
    }
]

USER_PROMPT = [
    {
        'type': 'list',
        'name': 'item',
        'message': 'What\'s next?',
        'choices': [
            SEND_A_MESSAGE,
            READ_MESSAGE,
            LIST_SENT_MESSAGES,
            LIST_UNPROCESSED_MESSAGES,
            LIST_MESSAGES_ON_MODERATION,
            LIST_APPROVED_MESSAGES,
            LIST_BLOCKED_MESSAGES,
            LIST_READ_MESSAGES,
            LIST_INCOMING_MESSAGES,
            BACK
        ]
    }
]


def login_validator(val):
    if not len(str(val).strip()):
        return 'Login cannot be empty'


class MenuScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.is_admin = self.state['user'].role.startswith('admin')

    def render(self):
        scenes = {
            SEND_A_MESSAGE: MessageCreationScreen,
            LIST_SENT_MESSAGES: ListSentScreen,
            LIST_UNPROCESSED_MESSAGES: ListCreatedScreen,
            LIST_MESSAGES_ON_MODERATION: ListModeratingScreen,
            LIST_APPROVED_MESSAGES: ListApprovedScreen,
            LIST_BLOCKED_MESSAGES: ListBlockedScreen,
            LIST_READ_MESSAGES: ListReadScreen,
            LIST_INCOMING_MESSAGES: ListIncomingMessagesScreen,
            MODERATE_MESSAGES: ModerationScreen,
            LIST_ACTIVE_SENDERS: ListActiveSendersScreen,
            LIST_ACTIVE_SPAMMERS: ListActiveSpammersScreen,
            LIST_ACTIONS_LOGS: ListActionLogsScreen,
            READ_MESSAGE: ReadMessageScreen
        }

        while True:
            answers = self.ask(ADMIN_PROMPT if self.is_admin else USER_PROMPT)
            if answers['item'] in scenes:
                scenes[answers['item']](self.state).render()
            else:
                return
