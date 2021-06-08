from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListBlockedScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.BLOCKED_MESSAGES_Z, self.state['user'].login)
