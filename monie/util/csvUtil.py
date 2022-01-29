import csv
import os
from shopify.util.configUtil import ConfigUtil
from shopify.util.dirUtil import DirUtil

class CsvUtil:

    configs = ConfigUtil()

    @staticmethod
    def generateCSV(fileName, data):
        keys = data[0].keys()

        dirPath = CsvUtil.configs.getConfig(['download', 'path'])
        if not DirUtil.isDir(dirPath):
            DirUtil.makeDir(dirPath)

        fullPath = os.path.join(dirPath, fileName)
        fileHndlr = open(fullPath, "w")
        dictWriter = csv.DictWriter(fileHndlr, keys)
        dictWriter.writeheader()
        dictWriter.writerows(data)
        fileHndlr.close()

        return fullPath
