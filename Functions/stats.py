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

    def green_red_counter(self):
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

        # Skip first row because already using prev
        df = df[1:]

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

    # 4 types-
    # 1. Daily volatility (Open-Close)
    # 2. Daily movement (High - Low)
    # 3. day-day volatility(Close - Close),
    # 4. Pre Market (Close-Open)
    def volatility(self):
        df = self.stock

        total1 = 0
        total2 = 0
        total3 = 0
        total4 = 0

        prev = float(df[0:1]['Close'])
        for index, day in df.iterrows():
            open = day['Open']
            close = day['Close']
            high = day['High']
            low = day['Low']

            change1 = abs(close - open)
            change2 = abs(high - low)
            # For first row skip pre market and day-day
            if index != 0:
                change3 = abs(close - prev)
                change4 = abs(prev - open)
            else:
                change3 = 0
                change4 = 0

            total1 += change1
            total2 += change2
            total3 += change3
            total4 += change4
            prev = close

        days = len(df)
        vol1 = total1 / days
        vol2 = total2 / days
        vol3 = total3 / (days - 1)
        vol4 = total4 / (days - 1)

        self.stats['Daily Volatility'] = vol1
        self.stats['Daily Volatility Movement(high-low)'] = vol2
        self.stats['Day-Day Volatility'] = vol3
        self.stats['Pre Market Volatility'] = vol4

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

    def run_all(self):
        self.green_red_counter()
        self.streaks()
        self.volatility()
        return self.stats

class MarketStats:
    def gen_report(self):
        pass

    # For merging 2 stocks
    def merge(self, stock1, stock2):
        pass

    # For merging a list of stocks
    def combine(self, stocks=None, out_list='Merged.csv'):
        pass
