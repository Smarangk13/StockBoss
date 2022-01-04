import datetime
import time
import os
from Functions.APIInterface import Alpaca
from Functions.formatter import DatesFormat


class Collector:
    def __init__(self):
        self.stocks = []
        self.alert_grid = []

        dirs = os.listdir()
        if 'stocks' not in dirs:
            os.mkdir('stocks')

    @staticmethod
    def last_date(stock):
        try:
            fileName = 'stocks/' + stock + '.csv'
            fr = open(fileName, 'r')
            content = fr.readlines()
            last = content[-1]
            last = last.replace('\'', '')
            data = last.split(',')
            dd = data[0]
            mm = data[1]
            yyyy = data[2]
            # add logic to delete last line (data may be recorded before close

            return DatesFormat.easyRFC(dd, mm, yyyy)

        except:
            return '2011-01-01T12:00:00Z'

    def get_history(self, ticker):
        # Collect data from API
        start = self.last_date(ticker)

        end = datetime.datetime.now()
        end = DatesFormat.regulartrfc(end)

        AlpacaObj = Alpaca()
        res = AlpacaObj.get_daily_history(ticker, start, end)
        if 'bars' not in res:
            print('Error with response')
            print(ticker)
            print(res)
            return

        bars = res['bars']

        # Result might be multiple pages
        while 'next_page_token' in res and res['next_page_token'] is not None:
            next_page = res['next_page_token']
            res = AlpacaObj.get_daily_history(ticker, start, end, next_page)
            bars += res['bars']

        # Format and ave to csv
        outfile = 'stocks/' + ticker + '.csv'
        fileWriter = open(outfile, 'a')
        fileWriter.write('Date,Month,Year,Day,Open,High,Low,Close,Vol\n')
        for daily in bars:
            market_date = daily['t']
            dateList = dd, mm, yyyy, day = DatesFormat.rfc_list(market_date)
            fileWriter.write(str(dateList)[1:-1].replace(' ', ''))
            fileWriter.write(',')
            ohlcv = list(daily.values())[1:6]
            fileWriter.write(str(ohlcv)[1:-1].replace(' ', ''))
            fileWriter.write('\n')

        fileWriter.close()

    def get_all_history(self):

        # 200 api calls/60second limit
        for i, stock in enumerate(self.stocks):
            self.get_history(stock)
            print('Collecting ', stock)
            if (i % 150) == 0:
                time.sleep(70)

    def get_latest(self):
        pass

    def get_stock_list(self, filename='stocks/spy500.csv'):
        try:
            fr = open(filename, 'r')
            content = fr.readlines()
            fr.close()
            self.stocks = [tk.replace('\n', '').split(',')[0] for tk in content][1:]
            return self.stocks
        except FileNotFoundError:
            print('No file with stock list found')

    def alert_levels(self):
        file = 'stocks/alerts.txt'
        with open(file) as f:
            content = f.readlines()

        tickers = []
        lows = []
        highs = []
        for line in content:
            ticker, low, high = line.split(',')
            tickers.append(ticker)
            lows.append(low)
            highs.append(high)

        self.alert_grid = [tickers, lows, highs]


if __name__ == '__main__':
    Collect = Collector()
    # Collect.get_stock_list()
    Collect.get_history('MSFT')
