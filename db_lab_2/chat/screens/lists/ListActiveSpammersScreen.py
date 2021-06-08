from .ListBaseScreen import ListBaseScreen
from chat import constants


class ListActiveSpammersScreen(ListBaseScreen):
    def get_key(self):
        return constants.SPAMMERS_Z

    def fetch(self, start, end):
        return list(map(lambda t: '"%s" with %i spams' % (t[0], t[1]),
                        self.redis.zrange(self.get_key(), start, end, withscores=True)))
