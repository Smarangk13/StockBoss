import pandas as pd
from sklearn.linear_model import SGDClassifier
from stats import StockStats


def accuracy(test, real):
    l = len(test)
    pos = l

    correct = 0
    wrong = 0

    for i in range(l):
        if test[i] == real[pos]:
            correct += 1
        else:
            wrong += 1
        pos += 1

    print(correct, wrong)
    print('accuracy = ', correct / (correct + wrong) * 100)


class Predictor:
    def __init__(self, stock):
        self.stock = stock # Pandas df
        self.sgd_trained = False

    def sgd_train(self, split=60):
        test_size = int(len(self.stock) * 0.6)
        x_train = self.stock[['Month', 'Open', 'High', 'Low', 'Close', 'Volume']][:test_size]
        y_train = self.stock[['Score']][1:test_size + 1]

        x_train = x_train.astype({'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int})

        model = SGDClassifier(loss="hinge", penalty="l2", max_iter=15)
        model.fit(x_train, y_train)

        x_test = self.stock[['Month', 'Open', 'High', 'Low', 'Close', 'Volume']][test_size:]

        y_test = model.predict(x_test)
        labels = self.stock[['Score']]

        start = test_size
        correct = 0
        wrong = 0
        for i in range(len(y_test)):
            if y_test[i] == labels[start]:
                correct += 1
            else:
                wrong += 1
            start += 1

        print(correct, wrong)
        print('Model trained with accuracy = ', correct / (correct + wrong) * 100)

    def sgd_predict(self):
        if not self.sgd_trained:
            self.sgd_train()

    def create_nn(self):
        pass

    def nn_predict(self):
        pass

    def intuit(self):
        prob = 0.5
        stats = StockStats(self.stock)
        stats.run_all()

        pass