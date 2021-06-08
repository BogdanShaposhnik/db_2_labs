from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListApprovedScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.APPROVED_MESSAGES_Z, self.state['user'].login)
