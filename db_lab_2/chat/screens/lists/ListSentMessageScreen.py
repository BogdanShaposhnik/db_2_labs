from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListSentScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.SENT_MESSAGES_Z, self.state['user'].login)
