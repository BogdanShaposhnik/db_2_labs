from chat.screens.BaseViewerScreen import BaseViewerScreen
from chat import constants
import abc


class ListBaseScreen(BaseViewerScreen):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.redis = state['redis']
        self.key = self.get_key()

    @abc.abstractmethod
    def get_key(self):
        pass

    def load(self):
        items = self.fetch(self.cursor, self.cursor + self.items_per_page)
        if not len(items):
            return []
        else:
            return items

    def fetch(self, start, end):
        items = self.redis.zrange(self.key, start, end)
        return list(map(self.map_messages_statuses, items))

    def items_count(self):
        return self.redis.zcard(self.key)

    def map_messages_statuses(self, mid):
        status = self.redis.hget('%s:%s' % (constants.MESSAGES_STORAGE, mid), 'status')
        if status == constants.STATUS_MESSAGE_BLOCKED:
            return '️ "%s" %s' % (mid, status)
        elif status == constants.STATUS_MESSAGE_APPROVED:
            return ' "%s" %s' % (mid, status)
        else:
            return ' "%s" %s' % (mid, status)
