import json
from datetime import datetime, timedelta
from threading import Thread
from monie.logger.logger import logger
from monie.service.handler.baseHandler import BaseHandler
from monie.core.simulation import Simulation
from monie.core.player import Player

class GameRoomHandler(BaseHandler):

    simulation = Simulation()
    startingBalance = 10000
    Thread(target=simulation.runSim).start()
    stockAllData = {}

    def get(self, slug=None):
        logger.info('[GET] Request - {}'.format(self.request.path))
        slug = slug.upper()
        try:
            if slug == 'LEADERBOARD':
                response = self.getLeaderboard()
            elif slug == 'ALL-STOCK-DATA':
                response = self.getStocksAll()
            self.send_response(response)
            logger.info('[GET] Response - {}'.format(self.request.path))
        except Exception as e:
            logger.exception(e)
            self.throwError()

    def post(self, slug=None):
        logger.info('[POST] Request - {}'.format(self.request.path))
        slug = slug.upper()
        try:
            if slug == 'ADD-PLAYER':
                response = self.addPlayerToGame()
            elif slug == 'START-SIMULATION':
                response = self.startSimulation()
            elif slug == 'BUY':
                response = self.buy()
            elif slug == 'SELL':
                response = self.sell()
            elif slug == 'SIM-CONTROL':
                response = self.controlSim()
            self.send_response(response)
            logger.info('[POST] Response - {}'.format(self.request.path))
        except Exception as e:
            logger.exception(e)
            self.throwError()

    def controlSim(self):
        request = self.getRequestBody()
        simSpeed = request.get('simSpeed', None)
        simPause = request.get('simPause', None)
        if simPause is not None:
            GameRoomHandler.simulation.isSimRunning = not simPause
        if simSpeed is not None:
            GameRoomHandler.simulation.sleepTime = simSpeed
        return {
            'message': 'Sim update successful'
        }

    def getStocksAll(self):
        stockDict = {}
        currentDate = GameRoomHandler.simulation.currentDate
        if len(GameRoomHandler.stockAllData) == 0 and GameRoomHandler.simulation.marketDataProvider is not None and currentDate is not None:
            mk = GameRoomHandler.simulation.marketDataProvider.store

            for stock in list(mk.columns):

                if len(stockDict) >= 100:
                    break

                ts = list(mk.loc[:, stock])
                idxL = list(mk.index)
                seenDataAt = None

                for idx, _ in enumerate(ts):
                    if ts[idx] != 0 and seenDataAt is None:
                        seenDataAt = idx
                        break
                if seenDataAt is not None and currentDate - idxL[seenDataAt] > timedelta(days=10):
                    stockDict[stock] = {
                        'idx':idxL[seenDataAt:],
                        'ts': ts[seenDataAt:]
                    }

        return stockDict

    def getRequestBody(self):
        return json.loads(self.request.body)

    def addPlayerToGame(self):
        request = self.getRequestBody()
        p = Player()
        p.name = request['userName']
        p.startingBalance = GameRoomHandler.startingBalance
        p.addItemToPortfolio('CASH', p.startingBalance, p.startingBalance)
        GameRoomHandler.simulation.players.append(p)

    def startSimulation(self):
        request = self.getRequestBody()
        GameRoomHandler.simulation.setStartDate(request['startDate'])
        GameRoomHandler.simulation.setEndDate(request['endDate'])
        GameRoomHandler.simulation.startSim()
        return {
            'message': 'Start sim successful'
        }

    def getLeaderboard(self):
        leaderbd = {}
        currentDate = GameRoomHandler.simulation.currentDate
        leaderbd['date'] = currentDate
        leaderbd['table'] = []
        leaderbd['started'] = GameRoomHandler.simulation.started
        leaderbd['players'] = [x.name for x in GameRoomHandler.simulation.players]
        leaderbd['lineChart'] = {
            'index':[],
            'players':[]
        }
        if leaderbd['started']:
            for player in GameRoomHandler.simulation.players:
                leaderbd['table'].append({
                    'name': player.name,
                    'portfolio': player.calcBalance(self.getPricer(), currentDate)
                })
                indexList = [x[0] for x in player.historyPerf]
                valueList = [x[1] for x in player.historyPerf]
                leaderbd['lineChart']['index'] = indexList
                leaderbd['lineChart']['players'].append({
                    'name': player.name,
                    'series': valueList
                })
            leaderbd['table'].sort(key=lambda x: x['portfolio']['value'], reverse=True)
        return leaderbd

    def getPricer(self):
        return GameRoomHandler.simulation.marketDataProvider

    def buy(self):
        request = self.getRequestBody()
        buyer = request['user']
        stockName = request['stock']
        unit = request['units']
        currentDate = GameRoomHandler.simulation.getCurrentDate()
        value = self.getPricer().getValue(stockName, unit, currentDate)

        GameRoomHandler.simulation.isSimRunning = False
        player = GameRoomHandler.simulation.getPlayer(buyer)
        cashPlayer = player.getCash()['value']
        if value > cashPlayer:
            return {
                'message':'Not enough money'
            }
        player.addItemToPortfolio(stockName, unit, value)
        player.addLedgerItem(stockName, unit, value)
        player.addItemToPortfolio('CASH', -value, -value)
        GameRoomHandler.simulation.isSimRunning = True
        return {
            'message': 'Buy successful'
        }

    def sell(self):
        request = self.getRequestBody()
        seller = request['user']
        stockName = request['stock']
        unit = request['units']
        currentDate = GameRoomHandler.simulation.getCurrentDate()
        value = self.getPricer().getValue(stockName, unit, currentDate)

        GameRoomHandler.simulation.isSimRunning = False
        player = GameRoomHandler.simulation.getPlayer(seller)
        itemPlayer = player.portfolio[stockName]['units']
        if unit > itemPlayer:
            return {
                'message': 'Not enough units to sell'
            }
        player.addItemToPortfolio(stockName, -unit, -value)
        player.addLedgerItem(stockName, unit, value, buy=False)
        player.addItemToPortfolio('CASH', value, value)
        GameRoomHandler.simulation.isSimRunning = True
        return {
            'message': 'Sell successful'
        }











