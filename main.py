# Main To Run through all stocks of the day and start report best for today
from tkinter import messagebox, Tk
from Functions.APIInterface import *


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

    while True:
        time.sleep(300)
        print('Refreshing')
        # Update all stocks
        # Check alerts

    # Collect stock data
