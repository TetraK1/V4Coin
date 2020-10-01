import csv
import datetime as dt
import matplotlib.pyplot as plt

class CurrencyPair:
    def __init__(self, v1_amount, v2_amount, ratio=0.5):
        #ratio is v1 value / v2 value
        self.v1 = v1_amount
        self.v2 = v2_amount
        self.ratio = ratio

    def balance(self, v1_price, v2_price):
        #price is equal to v2/v1 i.e. number of v2 per v1
        total_value = self.v1 * v1_price + self.v2 * v2_price
        self.v1 = (total_value * self.ratio) / v1_price
        self.v2 = (total_value * (1-self.ratio)) / v2_price
        return self.v1, self.v2

    def get_total_value(self, v1_price, v2_price):
        return self.v1 * v1_price + self.v2 * v2_price


def get_data():

    with open('etherprice-from-etherscan.csv') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    data = data[1:] #remove column headings

    data = [
        [
            dt.datetime.fromtimestamp(int(i[1])),
            float(i[2])
        ] for i in data
    ]

    return data

data = get_data()[-365:] #only last year of prices
#data = data + data[::-1] #start and end at the same price
#data.append(data[0]) #crash to initial price right at the end

#example eth/usdt pair, starting with 100 usdt

if __name__ == '__main__':
    pools = [i/100 for i in range(0, 101)]
    pools = [CurrencyPair(0, 100, ratio=i) for i in pools]

    for date, price in data:
        for p in pools:
            p.balance(price, 1)

    final_price = data[-1][1]
    print('Ratio\tFinal ETH\tFinal USD\tFinal Total')
    for p in pools:
        #print(f'{p.ratio}\t{p.v1}\t{p.v2}\t{p.get_total_value(final_price, 1)}')
        print('{:.2f}\t{:.2f}\t\t{:.2f}\t\t{:.2f}'.format(p.ratio, p.v1, p.v2, p.get_total_value(final_price, 1)))

    plt.plot([p.ratio for p in pools], [p.get_total_value(final_price, 1) for p in pools])
    plt.ylabel('Total value (USD)')
    plt.xlabel('Balancing Ratio (ETH/USDT)')
    plt.title('Pool balancing ratio vs final total value')
    plt.show()