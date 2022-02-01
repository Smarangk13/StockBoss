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
            file_name = 'stocks/' + stock + '.csv'
            fr = open(file_name, 'r')
            content = fr.readlines()
            last = content[-1]
            last = last.replace('\'', '')
            data = last.split(',')
            dd = data[0]
            mm = data[1]
            yyyy = data[2]
            # add logic to delete last line (data may be recorded before close

            return DatesFormat.easyRFC(dd, mm, yyyy)

        except FileNotFoundError:
            return '2011-01-01T12:00:00Z'

    def get_history(self, ticker):
        # Collect data from API
        start = self.last_date(ticker)

        end = datetime.datetime.now()
        end = DatesFormat.regulartrfc(end)

        alpaca = Alpaca()
        res = alpaca.get_daily_history(ticker, start, end)
        if 'bars' not in res:
            print('Error with response')
            print(ticker)
            print(res)
            return res

        bars = res['bars']

        # Result might be multiple pages
        while 'next_page_token' in res and res['next_page_token'] is not None:
            next_page = res['next_page_token']
            res = alpaca.get_daily_history(ticker, start, end, next_page)
            bars += res['bars']

        # Format and ave to csv
        outfile = 'stocks/' + ticker + '.csv'

        if ticker + '.csv' not in os.listdir(os.getcwd() + "/stocks"):
            file_writer = open(outfile, 'a')
            file_writer.write('Date,Month,Year,Day,Open,High,Low,Close,Vol\n')

        else:
            file_writer = open(outfile, 'w')

        for daily in bars:
            market_date = daily['t']
            date_list = dd, mm, yyyy, day = DatesFormat.rfc_list(market_date)
            file_writer.write(str(date_list)[1:-1].replace(' ', ''))
            file_writer.write(',')
            ohlcv = list(daily.values())[1:6]
            file_writer.write(str(ohlcv)[1:-1].replace(' ', ''))
            file_writer.write('\n')

        file_writer.close()
        return True

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
    Collect.get_history('FB')
