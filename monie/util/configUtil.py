import os
import yaml
from monie.util.dirUtil import DirUtil
from monie.util.envUtil import EnvUtil

class ConfigUtil:

    config = None
    configFilePath = None
    isSetup = False

    def __init__(self, config=None, configFilePath=None):
        self.config = config
        self.configFilePath = configFilePath
        self.setup()

    def setup(self):
        if self.config is None:
            if self.configFilePath is None:
                self.configFilePath = ConfigUtil.getDefaultConfigFilePath()
            self.loadConfig()

    @staticmethod
    def getDefaultConfigFilePath():
        env = EnvUtil.getEnv()
        configFilePath = os.getenv('APP_CONFIG_PATH', None)
        if configFilePath is None:
            curentScriptDir = DirUtil.getCurrentScriptDirectory()
            projectDir = DirUtil.getParentDir(curentScriptDir)
            configFilePath = os.path.join(projectDir, 'resource', 'config', 'settings_{}.yaml'.format(env))
        else:
            configFilePath = os.path(configFilePath)
        return configFilePath

    def loadConfig(self):
        file = open(self.configFilePath)
        self.config = yaml.full_load(file)

    def getConfig(self, path):
        res = self.config
        for item in path:
            res = res.get(item)
        return res

if __name__ == '__main__':
    c = ConfigUtil()
    print(c.getConfig('database'))
