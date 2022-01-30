class Player:

    def __init__(self):
        self.name = None
        self.balance = None
        self.portfolio = {}
        self.startingBalance = None
        self.ledger = []
        self.historyPerf = []

    def addItemToPortfolio(self, stockName, units, value):
        if stockName in self.portfolio:
            existing = self.portfolio[stockName]
            existing['units'] += units
            existing['value'] += value

            if existing['units'] <= 0:
                del self.portfolio[stockName]
        else:
            self.portfolio[stockName] = {
                'units': units,
                'value': value
            }

    def addLedgerItem(self, stockName, units, value, buy=True):
        self.ledger.append("{} {} {} {}".format(stockName, 'BUY' if buy else 'SELL', units, value))

    def pushHistory(self, date, pricer):
        self.historyPerf.append((date, self.calcBalance(pricer, date)['value']))

    def getCash(self):
        return self.portfolio['CASH']

    def calcBalance(self, pricer, currentDate):
        balDict = {}
        totalSum = 0
        for item in self.portfolio:
            if item != 'CASH':
                balDict[item] = {
                    'originalValue': self.portfolio[item]['value'],
                    'currentValue': pricer.getValue(item, self.portfolio[item]['units'], currentDate),
                    'units': self.portfolio[item]['units']
                }
            else:
                balDict[item] = {
                    'originalValue': 10000,
                    'currentValue': self.portfolio[item]['value'],
                    'units': self.portfolio[item]['value']
                }
            totalSum += balDict[item]['currentValue']

        return {
            'value': totalSum,
            'assets': balDict,
            'pnl': (totalSum-10000)/10000 * 100
        }