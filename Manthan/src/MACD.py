class MACD(bt.Strategy):
	params=(('fast_LBP',12),('slow_LBP',26),('max_position',1),('signal_LBP',9))

	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		self.fast_EMA = EMA(self.data, period=self.params.fast_LBP)
		self.slow_EMA = EMA(self.data, period=self.params.slow_LBP)

		self.MACD=self.fast_EMA-self.slow_EMA
		self.Signal = EMA(self.MACD, period=self.params.signal_LBP)
		self.Crossing = bt.indicators.CrossOver(self.MACD,self.Signal,plotname='Buy_Sell_Line')
		self.Hist = self.MACD - self.Signal
		
	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
		# Buy/Sell order submitted/accepted to/by broker - Nothing to do
			return

		# Check if an order has been completed
		# Attention: broker could reject order if not enough cash
		if order.status in [order.Completed]:
			if order.isbuy():
				self.log('BUY EXECUTED, %.2f' % order.executed.price)
			elif order.issell():
				self.log('SELL EXECUTED, %.2f' % order.executed.price)

			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		# Write down: no pending order
		self.order = None

	def next(self):

		# If MACD is above Signal line
		if self.Crossing > 0:
			if self.position.size < self.params.max_position:
				self.buy()

		# If MACD is below Signal line
		elif self.Crossing < 0:
			if self.position.size > 0:
				self.close()