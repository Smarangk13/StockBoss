import pandas as pd

def avg(nums):
    total = 0
    for n in nums:
        total += n
    avg = total/ len(nums)
    return avg

class Stats:
    def __init__(self, stock):
        self.stock = stock # Pandas DF
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
        df= self.stock

        change = 0
        total = 0
        prev = float(df[0:1]['Close'])
        for index, day in df.iterrows():
            close = day['Close']
            change = abs(close - prev)
            total += change
            prev = close

        vol = total/len(df)
        self.stats['Volatility'] = vol