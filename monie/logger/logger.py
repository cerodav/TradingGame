import logging
import os
import datetime
from pathlib import Path
from monie.util.configUtil import ConfigUtil

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyLogger(object, metaclass=SingletonType):
    _logger = None

    def __init__(self):

        self._configUtil = ConfigUtil()
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()
        dirPath = Path(self._configUtil.getConfig(['log', 'path']))

        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)

        logFileAbsolutePath = os.path.join(dirPath, "log_" + now.strftime("%Y-%m-%d")+".log")
        fileHandler = logging.FileHandler(logFileAbsolutePath)

        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

        print("[LOGGER] Generating new logger instance")
        print("[LOGGER] Log files set to dump at : {}".format(logFileAbsolutePath))

    def get_logger(self):
        return self._logger

logger = MyLogger.__call__().get_logger()

if __name__ == "__main__":
    pass