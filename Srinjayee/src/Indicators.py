# Importing the necessary modules
from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import backtrader.indicators as btind
import datetime 

class MACD_Str(bt.Strategy):
    # parameters to be used in this strategy
    params = (('period1',12), ('period2',26), ('signal_period',9))
    
    def log(self, text, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s %s" %(dt.isoformat(), text))
        
    def __init__(self):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # add macd indicator
        self.macd = btind.MACD(self.data, period_me1=self.p.period1, \
                               period_me2=self.p.period2, period_signal=self.p.signal_period)
        self.crossover = btind.CrossOver(self.macd.macd, self.macd.signal)
    
    def next(self):
        # If an order is already pending we cannot send another one
        if self.order:
            return
        # Check if we are in the market
        if not self.position:
        # We are not in the market, look for a signal to OPEN trades
            # If the macd line is above the signal line
            if self.crossover > 0:
                self.log("Buy (Creating a long position) at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # Otherwise if the macd line is below the signal line 
            elif self.crossover < 0:
                self.log("Sell (Creating a long position) at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
        # if we are not in market
        # Check for positions to close trade
        
            # if it is a long position check for selling opportunity and close the postion
            if self.position.size>0 and  self.crossover<0:
                self.log("Closing the long postion at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.close()
            # if it is short position check for buying opportunity and close the postion
            elif self.position.size<0 and self.crossover>0:
                self.log("Closing the short postion at %s" % self.data.close[0])  
                #Keep track of the created order to avoid a 2nd order
                self.order = self.close()
        
    def notify_trade(self, trade):
        # if trade not completed yet no need to notify
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
    
    def notify_order(self, order):
        # if order is submitted/accepted then nothing to do
        if order.status in [order.Submitted, order.Accepted]:
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            # if there is an order to buy
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            # if there is an order to sell
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        # if order Rejected/canceled/Margin
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')
        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        # Reset
        self.order = None    

class RSI(bt.Strategy):
    #parameters to be  used in this strategy
    params = (('oversold_limit', 30), ('overbought_limit', 70),)
    
    def log(self, text, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s %s" %(dt.isoformat(), text))
        
    def __init__(self):
        # add a rsi indicator
        self.rsi = btind.RSI(self.data)
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
    def notify_order(self, order):
        
        # if order is submitted/accepted then nothing to do
        if order.status in [order.Submitted, order.Accepted]:
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            # if there is an order to buy
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            # if there is an order to sell
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        # if order Rejected/canceled/Margin
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')
        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        # Reset
        self.order = None
        
    def notify_trade(self, trade):
        # if trade not completed yet no need to notify
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %(trade.pnl, trade.pnlcomm))
    
    def next(self):
         # If an order is already pending we cannot send another one
        if self.order:
            return
        # if we are not in market
        # Check for positions to open trade
        if not self.position:
            # rsi in oversold region --> BUY!!
            if self.rsi< self.p.oversold_limit:
                self.log("Buy (Creating a long position) at %s" %self.data.close[0])
                self.order = self.buy()
            # rsi in overbought region --> SELL!!
            if self.rsi> self.p.overbought_limit:
                self.log("Sell (Creating a short position) at %s" %self.data.close[0])
                self.order = self.sell()
        else:
             # if it is a long position check for selling opportunity
            if self.position.size>0 and self.rsi > self.p.overbought_limit:
                self.log("Closing the long position at %s" %self.data.close[0])
                self.order = self.close()
            # else if it is short position check for buying opportunity
            if self.position.size<0 and self.rsi < self.p.oversold_limit:
                self.log("Closing the short postion at %s" %self.data.close[0])
                self.order = self.close()

class Boll_Bands(bt.Strategy):
    #parameters to be used in this strategy
    params = (('period', 30),('no_of_std', 3.0),)
    
    def log(self, text, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s %s" %(dt.isoformat(), text))
        
    def __init__(self):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # Add a BBand indicator
        self.bband = btind.BollingerBands(self.datas[0], period=self.p.period, devfactor=self.p.no_of_std)
    
    def notify_order(self, order):
        
        # if order is submitted/accepted then nothing to do
        if order.status in [order.Submitted, order.Accepted]:
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            # if there is an order to buy
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            # if there is an order to sell
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        # if order Rejected/canceled/Margin
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')
        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        # Reset
        self.order = None
        
    def notify_trade(self, trade):
        # if trade not completed yet no need to notify
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %(trade.pnl, trade.pnlcomm))
    
    def next(self):
        # If an order is already pending we cannot send another one
        if self.order:
            return
        # if we are not in market
        # Check for positions to open trade
        if not self.position:
            # if the close value is lower than bollinger low it is a buying opportunity 
            if self.data.close < self.bband.lines.bot:
                self.log("Buy (Creating a long position) at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # if the close value is greater than bollinger high it is a selling opportunity (Shorting)
            elif self.data.close > self.bband.lines.top:
                self.log("Sell (Creating a short position) at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        # if we are in market 
        # Check for positions to close trade
        else:
            # exiting the long position(Reaching the midline is a good target)
            if self.position.size>0 and self.data.close >= self.bband.lines.mid:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("Closing the long postion at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.close()
            # exiting the short position.(Reaching the midline is a good target)
            elif self.position.size<0 and self.data.close <= self.bband.lines.mid:
                #Buy
                self.log("Closing the short postion at %s" % self.data.close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.close()
