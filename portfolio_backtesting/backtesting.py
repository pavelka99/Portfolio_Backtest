from pandas.core.arrays import base
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


weighting1 = {"BTC-EUR":"6","AAPL":"10","AMD":"6","AMZN":"6","ASML":"6","BNGO":"6","CRWD":"6","DIS":"6","ETH-EUR":"6","FB":"6","GOOGL":"6","MSFT":"6",
"NFLX":"6","NIO":"6","PLTR":"6","TSLA":"6"}
weighting2 = {"BTC-EUR":"3","SPY":"97"}
weighting3 = {"BTC-EUR":"20","SPY":"50", "AAPL":"30"}

members = ["BTC-EUR", "SPY", "AMD", "AAPL","AMZN", "ASML", "BNGO", "CRWD", "DIS", "ETH-EUR", "FB", "GOOGL", "MSFT", "NFLX", "NIO", "PLTR", "TSLA"]


def PortfolioCalc(weightings, data, name):
    data[name] = sum([ int(weightings[x])*data[x]/100 for x in list(weightings.keys()) ])
    return data 

basedata = yf.Ticker(members[0]).history(period="max").reset_index()[["Date","Open"]]
basedata["Date"] = pd.to_datetime(basedata["Date"])
basedata = basedata.rename(columns = {"Open":members[0]})



if (len(members)>1):
  for x in range(1,len(members)):
    newdata = yf.Ticker(members[x]).history(period="max").reset_index()[["Date","Open"]]
    newdata["Date"] = pd.to_datetime(newdata["Date"])
    newdata = newdata.rename(columns = {"Open":members[x]})
    basedata = pd.merge(basedata, newdata, on="Date")

basedata = basedata[ basedata["Date"]> "2013-01-01"]

for x in members:
    basedata[x] = basedata[x]/(basedata[x].iloc[0])

basedata = PortfolioCalc(weighting1, basedata, "Portfolio1")
basedata = PortfolioCalc(weighting2, basedata, "Portfolio2")
basedata = PortfolioCalc(weighting3, basedata, "Portfolio3")

plt.plot(basedata["Date"], basedata["Portfolio1"], label = "Portfolio1")
plt.plot(basedata["Date"], basedata["Portfolio2"], label = "Portfolio2")
plt.plot(basedata["Date"], basedata["Portfolio3"], label = "Portfolio3")


plt.style.use("seaborn")
plt.legend(loc= "upper left")

plt.show()

print(basedata)  