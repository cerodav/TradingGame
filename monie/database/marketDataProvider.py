import os
import pandas as pd
from datetime import datetime, timedelta
from monie.util.dirUtil import DirUtil

class MarketDataProvider:

    def __init__(self, startDate, endDate):
        dir = DirUtil.getCurrentScriptDirectory()
        parent = dir.parent
        historyFilePath = os.path.join(parent, 'resource', 'data', 'history.csv')
        df = pd.read_csv(historyFilePath, skiprows=1).drop('0', 1).set_index('Timestamp')
        df.index = pd.to_datetime(df.index)
        self.startDate = pd.to_datetime(startDate)
        self.endDate = pd.to_datetime(endDate)
        self.store = df.loc[self.startDate + timedelta(days=-20):self.endDate, :]

    def getValue(self, stockName, unit, currentDate):
        return self.store.loc[currentDate, stockName] * unit


if __name__ == '__main__':
    m = MarketDataProvider('1-1-2000', '1-1-2010')
    pass