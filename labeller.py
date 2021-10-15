import pandas as pd

class Labeller:
    @staticmethod
    def simple(stock):
        labels = []
        for i in range(1, 100):
            last = stock['Close'][i-1]
            cur = stock['Close'][i]
            if cur - last > 0:
                score = 1
            else:
                score = -1

            labels.append(score)
        return labels