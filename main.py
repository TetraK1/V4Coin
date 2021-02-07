import math

class Pool:
    def __init__(self):
        self.usd = 0
        self.peg = 0
        self.eth = 0
        self.total_ot = 0

    def initialise(self, usd, peg, eth):
        self.usd = usd
        self.peg = peg
        self.eth = eth

        issued_ot = 1

        self.total_ot += issued_ot
        return issued_ot

    def get_price(self):
        return self.peg / self.eth

    def get_pool_value(self, peg=None, usd=None):
        peg = peg or self.peg
        usd = usd or self.usd
        return peg + usd

    def get_value_at_price(self, price):
        return self.eth * price + self.usd

    def buy(self, usd):
        assert usd > 0

        delta_eth = self.eth * (math.exp(-1 * usd / self.peg) - 1)

        assert delta_eth < 0
        self.usd += usd
        self.eth += delta_eth
        return -1 * delta_eth

    def sell(self, eth):
        assert eth > 0

        delta_usd = self.peg * math.log(self.eth / (self.eth + eth))

        assert delta_usd < 0
        self.eth += eth
        self.usd += delta_usd
        return -1 * delta_usd

    def join(self, eth):
        '''Add your eth to the pool, increase peg proportionally, and issue ot based on value increase'''
        assert eth > 0
        eth_value = eth * self.get_price()

        issued_ot = self.total_ot * (eth_value / self.get_pool_value())

        self.peg *= 1 + (eth / self.eth)
        self.eth += eth
        self.total_ot += issued_ot
        return issued_ot

    def leave(self, ot):
        '''Redeem ot and leave the pool, receive proportion of eth and usdt'''
        assert ot > 0

        ot_propotion = ot / self.total_ot
        eth = self.eth * ot_propotion
        usd = self.usd * ot_propotion

        self.eth -= eth
        self.usd -= usd
        self.total_ot -= ot
        self.peg *= 1 - (ot_propotion)
        return usd, eth

    def arbitrate_join(self, eth):
        '''Add eth to pool without affecting peg, receiving ot.
        
        normally normal join is desirable, except when pool price is above real price, in which case
        this method is a way of receiving the benefit of arbitrage
        '''
        assert eth > 0

        peg_ratio = self.peg / (self.peg + self.usd)
        c = self.total_ot / (self.eth ** peg_ratio)
        e1 = self.eth + eth
        o1 = c * (e1 ** peg_ratio)

        assert o1 > self.total_ot
        d_ot = o1 - self.total_ot

        self.total_ot += d_ot
        self.eth += eth
        return d_ot
        

    def __str__(self):
        return f'Pool: {self.usd:.3f}:{self.peg:.3f}:{self.eth:.3f}, Value: {self.get_pool_value():.3f}, Issued OT: {self.total_ot:.3f}, Price: {self.get_price():.3f}'

p = Pool()
p.initialise(1000, 800, 0.8)
real_price = 800

print()

print(p)
print('Starting real value:', p.get_value_at_price(800))
print()

ot = p.arbitrate_join(0.2)
print('Received ot:', ot)
print('Post-join real value', p.get_value_at_price(800))
print(p)
print()

r= p.leave(ot)
print('Received on leave:', r)
print('Leaving value:', r[0] + r[1] * real_price)
print('post-leave real value:', p.get_value_at_price(800))
print(p)
print()