from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListActiveSendersScreen(ListBaseScreen):
    def get_key(self):
        return constants.ACTIVE_SENDERS_Z

    def fetch(self, start, end):
        return list(map(lambda t: '"%s" with %i messages' % (t[0], t[1]),
                        self.redis.zrange(self.get_key(), start, end, withscores=True)))
