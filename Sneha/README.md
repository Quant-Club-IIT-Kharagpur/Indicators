Backtesting indicators on MSFT stock prices during the period from 2016-2019

# Technical Indicators
The traders use indicators to predict the future value of a security by analysing its price movement.
You can read more about indicators here: https://www.investopedia.com/terms/t/technicalindicator.asp


The indicators used in this repo are:

### Exponential Moving Average (EMA):
Moving averages are very elementary indicators. The average is the arithmetic mean of a given set of prices over the specific number of days in the past. Moving average calculates the average of a fixed number past data points of at a given point of time. As we move ahead in time, the latest values are included in the moving average, and the oldest values are removed.
A simple moving average(SMA) gives equal weightage to all the data points, whereas an exponential moving average (EMA) gives more weightage to the most recent data points. Due to this, EMA is more responsive to price changes, and thus traders prefer it more than SMA.
You can read more about moving averages here: https://www.investopedia.com/terms/m/movingaverage.asp

### Moving Average Crossover:
Moving averages may result in difficult situations and sometimes heavy losses when there is no trend in the market. To overcome this, a moving average crossover system is adopted.
In this, two EMAs are used – one with a shorter period and the other with a longer period. The shorter EMA is faster to react, while the longer EMA is slower to react. 
When the shorter/faster EMA crosses and goes above the longer/slower EMA, it shows an uptrend, and it indicates a good buying opportunity. Similarly, when the shorter/faster EMA crosses and goes below the longer/slower EMA, it shows a downtrend, and it indicates a selling opportunity.
You can read more about moving average crossover here:
https://www.investopedia.com/terms/c/crossover.asp

### Moving Average convergence Divergence (MACD):
As the name suggests, MACD is all about the convergence ( when the two moving averages move towards each other )  and divergence (when the moving averages move away from each other )of the two moving averages. Similar to Moving Average Crossover, we use two EMAs in this indicator as well – one with a shorter period and the other with a longer period. We subtract the longer period EMA from the shorter period EMA to estimate the value of convergence/divergence or the MACD value. By plotting a graph of MACD values, we get the MACD line. MACD is positive/negative depending upon whether the shorter period moving average is above/below the longer period moving average. A negative value of MACD signifies downward trend, whereas a positive value shows an uptrend. Apart from the MACD line it also has another Signal Line which is the EMA of the MACD line. When the MACD line goes above the signal line, then traders look for buying opportunity, and when it goes below Signal line, then the traders look for selling opportunity.

Read more about this here: 	https://www.investopedia.com/terms/m/macd.asp


### Relative Strength Index (RSI): 
This is a prevalent indicator used to identify trend reversal. Although the term is relative strength index, it shows the internal strength of the security and not the relative strength. 

Formula:
RSI = 100 - 100/(1+RS)
RS = Average Gain/ Average Loss

The value of RSI lies between 0 and 100. A value between 0 and 30 is considered oversold. Hence the trader should look at buying opportunities.
A value between 70 and 100 is considered overbought. Hence the trader should look at selling opportunities.
Read more about this here: https://www.investopedia.com/terms/r/rsi.asp


### Bollinger Bands:
Bollinger bands consist of three lines – the middle line ,the upper line and the lower line. The middle line is the SMA of the closing prices. Typically, the upper and lower bands are 2 standard deviations away from the SMA line. The standard deviation shows the volatility of the stock.  During the period of low volatility, the Bollinger bands tighten and indicate that there might be a trend reversal whereas during high volatility period they expand and indicate the end of the existing trend. Most of times the prices stay within the two bands and we trade based on how price lies relative to these bands.
Read more about this here:	https://www.investopedia.com/terms/b/bollingerbands.asp
