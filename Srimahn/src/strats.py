import backtrader as bt
import datetime

class BB(bt.Strategy):
    params = (
        ('tperiod', 21),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.tperiod)
        self.pch = bt.indicators.PercentChange(self.datas[0], period = 1)
        self.boll = bt.indicators.BollingerBands(
            self.pch, period=self.params.tperiod, devfactor = 2.5)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f \n' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            if self.pch[-1] < self. boll.lines.bot[-1]:
                if self.dataclose[0] > self.dataclose[-1] and (self.boll.lines.top[0]-self.boll.lines.bot[0]) > 0.03 :

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

        else:

            if self.dataclose[-1] > self.sma[-1] and self.dataclose[0]< self.sma[0]:
                
                self.log('Sell CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class RSI_GCross(bt.Strategy):
    params = (
        ('stperiod', 5), ('ltperiod', 21), ('rsitperiod',5)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.signal = 0

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0].close, period = self.params.stperiod)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.datas[0].close, period = self.params.rsitperiod)
        self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0].close, period = self.params.ltperiod)
        self.cross = bt.indicators.CrossOver(self.sma, self.ema)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f \n' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            
            if self.rsi[0] > 70:
                if (self.cross[0] == 1) :

                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                    self.signal = -1
                    self.order = self.sell()

            elif self.rsi[0] < 30:
                if (self.cross[0] == -1) :

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    self.signal = 1
                    self.order = self.buy()

        else:  #for checking exit conditions
            if self.signal < 0:
                if self.rsi[0]<= 35 :
                    
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    self.signal = 0
                    self.order = self.buy()

            else:
                if self.rsi[0] >= 65 :
                
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                    self.signal = 0
                    self.order = self.sell()
                   