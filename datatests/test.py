import csv
import datetime as dt

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

redata = data[-365:]
#redata = redata + redata[::-1] #start and end at the same price
redata.append(redata[0]) #crash to initial price right at the end

#example eth/usdt pair, starting with 100 usdt

pools = [i/20 for i in range(0, 21)]
pools = [CurrencyPair(0, 100, i) for i in pools]

for date, price in redata:
    for p in pools:
        p.balance(price, 1)

final_price = redata[-1][1]
print('Ratio\tFinal ETH\tFinal USD\tTotal')
for p in pools:
    #print(f'{p.ratio}\t{p.v1}\t{p.v2}\t{p.get_total_value(final_price, 1)}')
    print('{:.2f}\t{:.2f}\t\t{:.2f}\t\t{:.2f}'.format(p.ratio, p.v1, p.v2, p.get_total_value(final_price, 1)))