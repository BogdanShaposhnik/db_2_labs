from chat import constants


class User:
    def __init__(self, login, role, redis):
        self.login = login
        self.role = role
        self.redis = redis
        p = self.redis.pipeline()
        p.lpush(constants.LIST_ACTION_LOGS, 'user "%s" login' % self.login)
        p.zincrby(constants.ONLINE_USERS_Z, 1, self.login)
        p.execute()

    def __del__(self):
        p = self.redis.pipeline()
        p.lpush(constants.LIST_ACTION_LOGS, 'user "%s" logout' % self.login)
        p.zincrby(constants.ONLINE_USERS_Z, -1, self.login)
        results = p.execute()
        if not results[1]:
            self.redis.zrem(constants.ONLINE_USERS_Z, self.login)

    @staticmethod
    def get_all_users_logins(redis):
        return list(map(lambda v: ''.join(v.split(':')[1:]), redis.keys('%s:*' % constants.USERS_STORAGE)))

    @staticmethod
    def load(redis, login):
        user = redis.hgetall('%s:%s' % (constants.USERS_STORAGE, login))
        if not user:
            return None
        return User(user['login'], user['role'], redis)

    def save(self):
        p = self.redis.pipeline()
        p.hmset('%s:%s' % (constants.USERS_STORAGE, self.login), {'login': self.login, 'role': self.role})
        p.execute()
