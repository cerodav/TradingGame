import time
from monie.database.marketDataProvider import MarketDataProvider
from datetime import datetime

class Simulation:

    def __init__(self):
        self.players = []
        self.currentDate = None
        self.startDate = None
        self.endDate = None
        self.isSimRunning = False
        self.sleepTime = 10
        self.marketDataProvider = None
        self.started = False

    def setStartDate(self, date):
        self.startDate = date

    def setEndDate(self, date):
        self.endDate = date

    def setCurrentDate(self, date):
        self.currentDate = date

    def getPlayers(self):
        return self.players

    def getCurrentDate(self):
        return self.currentDate

    def startSim(self):
        self.marketDataProvider = MarketDataProvider(self.startDate, self.endDate)
        self.dateList = [x for x in list(self.marketDataProvider.store.index) if x > datetime(2000, 1, 1)]
        self.isSimRunning = True
        self.started = True

    def setMarketDataProvider(self, m):
        self.marketDataProvider = m

    def getPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def runPlayerPerfHistory(self):
        for player in self.players:
            player.pushHistory(self.currentDate, self.marketDataProvider)

    def runSim(self):
        i = 0
        while True:
            time.sleep(self.sleepTime)
            if self.isSimRunning:
                self.setCurrentDate(self.dateList[i])
                self.runPlayerPerfHistory()
                if i == len(self.dateList)-1:
                    self.isSimRunning = False
                    break
                else:
                    i += 1
