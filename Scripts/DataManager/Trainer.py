from pandas import DataFrame

from Scripts.DataManager.MySQLManager import MySQLManager
from Scripts.DataManager.YahooAPIHandler import YahooAPIHandler
from Scripts.DataManager.BaseLines import average, seasonal_naive, drift

from datetime import datetime
import math
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.api import ARIMA
from statsmodels.iolib.table import SimpleTable
from statsmodels.tools.eval_measures import rmse, meanabs
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from stockstats import StockDataFrame


def run():
    # Definindo ticker
    ticker = {"Inter": "BIDI4.SA",
              "Petrobras": "PETR4.SA",
              "Vale": "VALE3.SA",
              "Itau": "ITUB4.SA",
              "Ambev": "ABEV3.SA",
              "Sinqia": "SQIA3.SA",
              "iShares_Bovespa": "BOVA11.SA"}

    currentTicker = ticker['Itau']

    mySQLManager = MySQLManager("localhost", "root", "toor")

    mySQLManager.connect("stock_market")
    dataSet = mySQLManager.read(table_name="stock", ticker=currentTicker, where_condition="date < \'2019-07-12\'", verbose=False)

    values = [float(x) for x in dataSet.values()]
    timeSerie = pd.Series(data=values, index=dataSet.keys(), name=str(currentTicker)+" stock time serie")

    fit1 = ExponentialSmoothing(timeSerie.values, seasonal_periods=5, trend='add', seasonal='add', damped=True).fit(use_boxcox=False)
    forecast = [x for x in fit1.forecast(120)]

    #fit1_arima = ARIMA(endog, order, exog=None, dates=None, freq=None, missing='none')
    #fit1_arima = ARIMA(data=values,)

    mySQLManager = None
    mySQLManager = MySQLManager("localhost", "root", "toor")
    mySQLManager.connect("stock_market")
    true_values = mySQLManager.read(table_name="stock", ticker=currentTicker,
                                    where_condition="date >= \'2019-07-12\' limit 120", verbose=False)


    #stockstats
    #open, close, high, low, volume, amount.
    dataFrame = pd.read_csv('/home/andromeda/programacao/TCC/StockMarketSwingTradeBot/Resources/Datasets/stock_market_stock.csv')
    stock = StockDataFrame.retype(dataFrame)






    #forecastOnTheTable = SimpleTable(data=[str(x) for x in forecast], title=str(currentTicker)+" stock time serie")
    #print(forecastOnTheTable.as_text())





    plt.plot([x for x in true_values.values()], '-k')
    plt.plot(forecast, '-g')
    plt.plot(average(timeSerie, 120), '-r')
    plt.plot(seasonal_naive(timeSerie, 5, 120), '-b')
    plt.plot(drift(timeSerie, 120), '-y')






    print("\tPrediction model\t\t|\tRMSE\t\t\t\t|\tMAE")
    print("\t---------------------------------------------------------------------")
    print("\tExponentialSmoothing", end="\t|\t")
    print(rmse([float(x) for x in true_values.values()], forecast), end="\t|\t")
    print(meanabs([float(x) for x in true_values.values()], forecast))

    print("\tSeasonal Naive", end="\t\t\t|\t")
    print(rmse([float(x) for x in seasonal_naive(timeSerie, 5, 120)], forecast), end="\t|\t")
    print(meanabs([float(x) for x in true_values.values()], seasonal_naive(timeSerie, 5, 120)))

    print("\tDrift", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in true_values.values()], drift(timeSerie, 120)), end="\t|\t")
    print(meanabs([float(x) for x in true_values.values()], drift(timeSerie, 120)))

    print("\tAverage", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in true_values.values()], average(timeSerie, 120)), end="\t|\t")
    print(meanabs([float(x) for x in true_values.values()], average(timeSerie, 120)))

if __name__ == "__main__":
    run()
