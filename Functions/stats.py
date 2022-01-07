import pandas as pd


def avg(nums):
    total = 0
    for n in nums:
        total += n
    average = total / len(nums)
    return average


class StockStats:
    def __init__(self, stock):
        self.stock = stock  # Pandas DF
        self.stats = {}

    def dailyStats(self):
        df = self.stock
        red_days = 0
        green_days = 0

        prev = float(df[0:1]['Close'])

        for index, day in df.iterrows():
            close = day['Close']

            if close > prev:
                green_days += 1

            else:
                red_days += 1

            prev = close

        self.stats['Green Days'] = green_days
        self.stats['Red Days'] = red_days

    def streaks(self):
        df = self.stock

        prev = float(df[0:1]['Close'])

        longest_red_streak = 0
        longest_green_streak = 0

        green_streak = 0
        red_streak = 0

        greens = []
        reds = []

        for index, day in df.iterrows():
            close = day['Close']

            if close > prev:
                if red_streak > 0:
                    reds.append(red_streak)
                red_streak = 0
                green_streak += 1
                if green_streak > longest_green_streak:
                    longest_green_streak = green_streak
            else:
                if green_streak > 0:
                    greens.append(green_streak)
                green_streak = 0
                red_streak += 1
                if red_streak > longest_red_streak:
                    longest_red_streak = red_streak

            prev = close

        self.stats["longest green"] = longest_green_streak
        self.stats["longest red"] = longest_red_streak
        avg_green = avg(greens)
        avg_red = avg(reds)
        self.stats["Avg green"] = avg_green
        self.stats["Avg red"] = avg_red

    def volatility(self):
        df = self.stock

        change = 0
        total = 0
        prev = float(df[0:1]['Close'])
        for index, day in df.iterrows():
            close = day['Close']
            change = abs(close - prev)
            total += change
            prev = close

        vol = total / len(df)
        self.stats['Volatility'] = vol

    def toMonth(self):
        df = self.stock
        cur_month = 0
        month_df = {}
        new_row = {}
        for index, row in df.iterrows():
            month = row['month']
            if month != cur_month:
                month_df[cur_month] = new_row
                cur_month = month

                new_row['Open'] = row['Open']
                new_row['High'] = row['High']
                new_row['Low'] = row['Low']
                new_row['Volume'] = 0

            if row['High'] > new_row['High']:
                new_row['High'] = row['High']

            if row['Low'] < new_row['Low']:
                new_row['Low'] = row['Low']

            new_row['Volume'] += row['Volume']
            new_row['Close'] = row['Close']

    def toWeek(self):
        pass

    def moving_avg(self, window, frame='Day'):
        if frame == 'Week':
            window *= 7
        elif frame == 'Month':
            window *= 30

    # Finds time periods for % change
    def change_find(self, change, tolerance=None):
        pass

    def slope_graph(self):
        pass


class MarketStats:
    def gen_report(self):
        pass

    # For merging 2 stocks
    def merge(self, stock1, stock2):
        pass

    # For merging a list of stocks
    def combine(self, stocks=None, out_list='Merged.csv'):
        pass
