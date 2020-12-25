Financial Indicators in Python using the package BackTrader

The following strategies have been implemented :
1. Golden Cross
2. Bollinger Bands
3. Stochastic Oscillator
4. Relative Strength Index + Ichimoku Clouds
5. Average Directional index

To learn about BackTrader, you can visit their document over [here](https://www.backtrader.com/docu/).

To try the indicators on other stocks, you can visit [Yahoo Finanace](https://in.finance.yahoo.com/) and search search the stock you want, go to historical data and set the required time period and download the data and convert the csv data to txt data. In the following code, you will need to change the name and the date in datetime(). For example, I have Apple's data from 1980-12-12 to 2020-9-4. So in the name string I have, name = "AAPL.txt". The date as, fromdate=datetime.datetime(1980,12,12),todate=datetime.datetime(2020, 9,4).
