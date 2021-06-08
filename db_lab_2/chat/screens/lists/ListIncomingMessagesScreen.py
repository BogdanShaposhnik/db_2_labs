from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListIncomingMessagesScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.INCOMING_MESSAGES_Z, self.state['user'].login)
