import os
import pathlib

class DirUtil:

    @staticmethod
    def getCurrentScriptDirectory():
        return pathlib.Path(__file__).parent.absolute()

    @staticmethod
    def getParentDir(path):
        return pathlib.Path(path).parent.absolute()

    @staticmethod
    def makeDir(path):
        return os.mkdir(path)

    @staticmethod
    def isDir(path):
        return os.path.isdir(path)

if __name__ == '__main__':
    p = DirUtil.getCurrentScriptDirectory()
    print(p)
    print(DirUtil.getParentDir(p))
