from Scripts.DataManager.MySQLManager import MySQLManager
from Scripts.DataManager.YahooAPIHandler import YahooAPIHandler

from datetime import datetime
import math
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf


def run():
    # Definindo ticker
    ticker = {"Inter": "BIDI4.SA", "Petrobras": "PETR4.SA", "Vale": "VALE3.SA", "Itau": "ITUB4.SA",
              "Ambev": "ABEV3.SA",
              "Sinqia": "SQIA3.SA", "iShares_Bovespa": "BOVA11.SA"}

    currentTicker = ticker['Itau']

    mySQLManager = MySQLManager("localhost", "root", "toor")
    mySQLManager.connect("stock_market")

    timeSerieValues = []
    timeSerieIndex = []
    for k, v in mySQLManager.read(table_name="stock", ticker=currentTicker, where_condition=None, verbose=False).items():
        timeSerieValues.append(float("{:7.5f}".format(v)))
        timeSerieIndex.append(k.strftime("%Y-%m-%d"))

    yf.pdr_override()
    DataFrame = pd.Series(data=timeSerieValues)  #, index=pd.DatetimeIndex(timeSerieIndex))


    fit1 = ExponentialSmoothing(DataFrame, seasonal_periods=5, trend='add', seasonal='add').fit(use_boxcox=False)
    results = pd.DataFrame(index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$\gamma$", r"$l_0$", "$b_0$", "SSE"])
    params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level', 'initial_slope']
    results["Additive"] = [fit1.params[p] for p in params] + [fit1.sse]
    ax = DataFrame.plot(figsize=(10, 6), marker='o', color='black',
                        title="Forecasts from Holt-Winters' multiplicative method")
    ax.set_ylabel("Stock price (R$)")
    ax.set_xlabel("Date")
    fit1.fittedvalues.plot(ax=ax, style='--', color='red')
    plt.show()


if __name__ == "__main__":
    run()
