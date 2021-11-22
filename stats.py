import pandas as pd


class Stats:
    def __init__(self, stock):
        self.stock = stock # Pandas DF
        self.stats = {}

    def dailyStats(self):
        df = self.stock
        red_days = 0
        green_days = 0
        longest_red_streak = 0
        longest_green_streak = 0

        prev = float(df[0:1]['Close'])
        for index, day in df.iterrows():
            close = day['Close']
            if close > prev:
                green_days += 1
            else:
                red_days += 1
            prev = close
