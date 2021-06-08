from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListModeratingScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.MESSAGES_ON_MODERATION_Z, self.state['user'].login)
