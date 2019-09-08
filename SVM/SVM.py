import numpy as np
import sys


class SVM():
    def __init__(self, x, y, epochs=200, learning_rate=0.0001):
        self.x = np.c_[np.ones(x.shape[0]), x]
        self.y = y
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.w = np.random.uniform(size=np.shape(self.x)[1])

    def get_loss(self, x, y):
        loss = max(0, 1 - y * np.dot(x, self.w))
        return loss

    def cal_sgd(self, x, y, w):
        if y * np.dot(x, w) < 1:
            w = w - self.learning_rate * (-y * x) - self.learning_rate * w
        else:
            w = w
        return w

    def train(self):
        for epoch in range(self.epochs):
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            for xi, yi in zip(x, y):
                loss += self.get_loss(xi, yi)
                self.w = self.cal_sgd(xi, yi, self.w)
            # print('epoch: {0} loss {1}'.format(epoch, loss))

    def predict(self, x):
        x_predict = np.c_[np.ones((x.shape[0])), x]
        result = int(np.sign(np.dot(x_predict, self.w)))
        print(result)
        return result


def readData(train_data_abspath):
    x = []
    y = []
    train_data_file = open(train_data_abspath)
    train_data_line = train_data_file.readline()
    while(train_data_line):
        line = train_data_line.split()
        data = []
        for i in range(len(line)-1):
            data.append(float(line[i]))
        num = float(line[-1])
        x.append(data)
        y.append(num)
        train_data_line = train_data_file.readline()
    return np.array(x), np.array(y)


if __name__ == '__main__':
    '''
    Main
    '''
    train_data_abspath = str(sys.argv[1])
    test_data_abspath = str(sys.argv[2])
    time_budget = int(sys.argv[4])

    # Train Model
    x_train, y_train = readData(train_data_abspath)
    svm = SVM(x_train, y_train)
    svm.train()

    # Test
    x_test, y_test = readData(test_data_abspath)
    crct_num = 0
    for i, test_data in enumerate(x_test):
        y_predict = svm.predict(np.mat(test_data))
        if y_predict == y_test[i]:
            crct_num += 1
