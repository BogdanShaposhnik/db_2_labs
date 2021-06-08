from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListReadScreen(ListBaseScreen):
    def get_key(self):
        return '%s:%s' % (constants.READ_MESSAGES_Z, self.state['user'].login)
