import redis
from chat.screens.StartScreen import StartScreen
from chat.config import redis_config


def worker(message):
    print(message)


def main():
    r = redis.Redis(host=redis_config['host'],
                    port=redis_config['port'],
                    db=redis_config['db'],
                    charset="utf-8",
                    decode_responses=True)
    state = {
        'redis': r
    }
    StartScreen(state).render()


if __name__ == '__main__':
    main()
