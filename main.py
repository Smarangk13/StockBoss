# Main To Run through all stocks of the day and start report best for today
import time
from tkinter import messagebox, Tk
from dataCollect import *

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
    crypto.update()

    while True:
        time.sleep(300)
        print('Refreshing')
        crypto.update()
        price = crypto.latest_price('BTC')
        if price < 61000:
            alert('SELL','HEY BTC IS BELOW 61k')
    # Collect stock data
