# Main To Run through all stocks of the day and start report best for today
import os
import pandas as pd
from tkinter import messagebox, Tk
from Functions.APIInterface import *
from Functions.stats import StockStats, MarketStats
from datacollector import Collector


def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)


if __name__ == '__main__':
    print('Welcome to stock boss')
    print('Calculating best stocks for today')

    # Prepare alert box
    Tk().withdraw()

    # Collect crypto Data
    crypto = Coinbase()

    stock = None

    while True:
        print('\nEnter an action')
        print('1. Select/Change Stock')
        print('2. Get Stats')
        print('3. Generate market report')
        print('4. Run Alerts')
        choice = int(input('\n'))

        if choice == 1:
            stock = input('Enter stock ticker:').upper()
            cwd = os.getcwd()
            stockdir = cwd + '/stocks'
            file = stock + '.csv'
            if file in os.listdir(stockdir):
                print('Found')
            else:
                print('Not found')
                print('Trying to download')
                collector = Collector()
                collector.get_history(stock)

        if choice == 2:
            if stock is None:
                print('No file selected')
                continue

            file = 'stocks/' + stock + '.csv'
            stockdf = pd.read_csv(file)
            print('Loaded stock-')
            print(stockdf.head())
            stats = StockStats(stockdf)
            results = stats.run_all()
            print(results)

        elif choice == 4:
            time.sleep(300)
            print('Refreshing')

        elif choice == 0:
            break
        # Update all stocks
        # Check alerts

    # Collect stock data
