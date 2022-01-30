import os

class EnvUtil:

    @staticmethod
    def getEnv(default='prod'):
        env = os.getenv('APP_ENV', None)
        if env is None:
            os.environ['APP_ENV'] = default
        return os.getenv('APP_ENV')
