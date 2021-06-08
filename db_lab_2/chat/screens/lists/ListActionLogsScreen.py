from chat.screens.BaseViewerScreen import BaseViewerScreen
from chat import constants


class ListActionLogsScreen(BaseViewerScreen):
    def __init__(self, state):
        super().__init__(items_per_page=25)
        self.state = state
        self.redis = self.state['redis']
        self.selected_message = None

    def get_key(self):
        return constants.LIST_ACTION_LOGS

    def fetch(self, start, end):
        return self.redis.lrange(self.get_key(), start, end)

    def items_count(self):
        return self.redis.llen(self.get_key())
