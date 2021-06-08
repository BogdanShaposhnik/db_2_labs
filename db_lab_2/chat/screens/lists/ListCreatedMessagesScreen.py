from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListCreatedScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.WAIT_FOR_MODERATION_MESSAGES_Z, self.state['user'].login)
