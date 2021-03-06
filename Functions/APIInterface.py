import requests
import random
import apiConfig
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class Alpaca:
    def __init__(self):
        # self.ALPACA_ENDPOINT = "https://paper-api.alpaca.markets"
        self.ALPACA_DATA_ENDPOINT = "https://data.alpaca.markets"
        self.HEADERS = {'APCA-API-KEY-ID': apiConfig.ALPACA_KEY,
                        'APCA-API-SECRET-KEY': apiConfig.ALPACA_SECRET_KEY}
        self.TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    def get_daily_history(self, symbol, start='2015-1-1T07:20:50.52Z', end='2021-1-1T07:20:50.52Z', page=None):
        ticker = symbol
        base_url = self.ALPACA_DATA_ENDPOINT
        data_url = "{}/v2/stocks/{}/bars".format(base_url, ticker)
        # data_url = "https://data.alpaca.markets/v2/stocks/MSFT/bars"
        params = {'start': start,
                  'end': end,
                  'timeframe': '1Day'}

        if page is not None:
            params['page_token'] = page

        r = requests.get(data_url, headers=self.HEADERS, params=params)
        json_hist_data = r.json()
        return json_hist_data

    # Gets granular data for today, might need to build more logic so that if it's a weekend,
    # We show Friday data (maybe this can be done from the front end? We get a few days' worth
    # of data here
    def get_granular_today_data(self, symbol, timeframe='minute'):
        history_url = "{}/v1/bars/{}?symbols={}&limit={}&start={}".format(self.ALPACA_DATA_ENDPOINT, timeframe, symbol,
                                                                          '600', self.TODAY)
        r = requests.get(history_url, headers=self.HEADERS)
        json_data = r.json()

        return json_data


class AlphaVantage:
    def __init__(self):
        self.baseURL = 'https://www.alphavantage.co/query?'
        self.__apikey = apiConfig.ALPHA_KEY

    """Better to call get current which uses this. Format is like this 
       {'Meta Data': 
       {'1. Information': 'Intraday (1min) open, high, low, close prices and volume', 
       '2. Symbol': 'AAPL', 
       '3. Last Refreshed': '2020-11-10 20:00:00', 
       '4. Interval': '1min', 
       '5. Output Size': 'Compact', 
       '6. Time Zone': 'US/Eastern'}, 
       'Time Series (1min)': {
       '2020-11-10 20:00:00': {'1. open': '116.0000', 
                               '2. high': '116.0800', 
                               '3. low': '116.0000', '
                               4. close': '116.0500', 
                               '5. volume': '14250'}, 
       '2020-11-10 19:59:00':... 
       """

    def get_daily(self, symbol, interval='1min'):
        modifiers = 'function=TIME_SERIES_INTRADAY' \
                    '&symbol=' + symbol + \
                    '&apikey=' + self.__apikey + \
                    '&interval=' + interval + \
                    '&outputsize=compact'

        request_url = self.baseURL + modifiers
        data = requests.get(request_url).json()

        return data

    # Returns current date-time and close value
    # Example ('2020-11-10 20:00:00', 116.05)
    def get_current(self, symbol):
        current_code = 'Time Series (1min)'
        data = self.get_daily(symbol)

        if current_code not in data:
            mod = random.randint(0, 350)
            default_num = 123.45 + mod
            return '2020-11-10 20:00:00', default_num

        data = data[current_code]
        day = next(iter(data))
        close = data[day]['4. close']

        if close is None:
            mod = random.randint(0, 350)
            default_num = 123.45 + mod
            return '0', default_num

        return day, float(close)


class Coinbase:
    def __init__(self):
        self.results = {}

    def latest_price(self, symbol):
        data = self.results
        for crypto in data['data']:
            if crypto['symbol'] == symbol:
                price = crypto['quote']['USD']['price']
                return price

    def update(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': apiConfig.Cryptokey,
        }

        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            self.results = data
            # print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


if __name__ == '__main__':
    Coins = Coinbase()
    Coins.update()
    print(Coins.results)
