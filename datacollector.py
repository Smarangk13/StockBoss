class Colletcor:
    def get_history(self):
        pass

    def get_latest(self):
        pass

    def get_stock_list(self):
        fileName = 'tickers.txt'
        fr = open(fileName,'r')
        content = fr.readlines()
        self.stocks = [tk.replace('\n','') for tk in content]
        print(self.stocks)


if __name__ == '__main__':
    Collect = Colletcor()
    Collect.get_stock_list()

