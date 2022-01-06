from sklearn.linear_model import SGDClassifier


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
    def sgd(self, stock, split=60):
        test_size = int(len(stock) * 0.6)
        X_train = stock[['Month', 'Open', 'High', 'Low', 'Close', 'Volume']][:test_size]
        Y_train = stock[['Score']][1:test_size + 1]

        X_train = X_train.astype({'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int})

        model = SGDClassifier(loss="hinge", penalty="l2", max_iter=15)
        model.fit(X_train, Y_train)

        X_test = stock[['Month', 'Open', 'High', 'Low', 'Close', 'Volume']][test_size:]

        Y_test = model.predict(X_test)
        labels = stock[['Score']]

        start = test_size
        correct = 0
        wrong = 0
        for i in range(len(Y_test)):
            if Y_test[i] == labels[start]:
                correct += 1
            else:
                wrong += 1
            start += 1

        print(correct, wrong)
        print('Model trasined with accuracy = ', correct / (correct + wrong) * 100)
