from pandas import DataFrame
import xgboost as xgb

from Scripts.DataManager.MySQLManager import MySQLManager
from Scripts.DataManager.YahooAPIHandler import *
from Scripts.DataManager.BaseLines import average, seasonal_naive, drift

import pandas as pd
from stockstats import StockDataFrame

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

def run(training_data: pd.DataFrame, test_data: pd.DataFrame):
    print(training_data.dtypes)
    print("\n")
    print(training_data.columns)

    #TODO: Adaptar para usar DataFrame de entrada
    training_data_serie = pd.Series(
                    data = training_data['adj close'],
                    index = training_data.index
    )
    test_data_serie = pd.Series(
                    data = test_data['adj close'],
                    index = test_data.index
    )

    debug(
        test_data= test_data_serie,
        forecast_ets= ets(training_data_serie, 120),
        forecast_arima= arima(training_data_serie, 120),
        forecast_xgboost= None,
        forecast_snaive= seasonal_naive(training_data_serie, 5, 120),
        forecast_drift= drift(training_data_serie, 120),
        forecast_average= average(training_data_serie, 120)
    )

def ets(time_serie, Npt):
    ets_fit = ExponentialSmoothing(time_serie.values, seasonal_periods=5, trend='add', seasonal='add', damped=True).fit()
    forecast_ets = [x for x in ets_fit.forecast(Npt)]
    return forecast_ets

def arima(time_serie, Npt):
    arima_fit = ARIMA(time_serie.values, (1, 1, 1)).fit()
    forecast_arima = [x for x in arima_fit.forecast(Npt)[0]] # [0]= predições
    return forecast_arima

def xgboost():
    # # read in data
    # dtrain = xgb.DMatrix('demo/data/agaricus.txt.train')
    # dtest = xgb.DMatrix('demo/data/agaricus.txt.test')
    # # specify parameters via map
    # param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
    # num_round = 2
    # bst = xgb.train(param, dtrain, num_round)
    # # make prediction
    # preds = bst.predict(dtest)
    pass

def debug(test_data, forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average):
    print("\tPrediction model\t\t|\tRMSE\t\t\t\t|\tMAE")
    print("\t---------------------------------------------------------------------")
    print("\tExponentialSmoothing", end="\t|\t")
    print(rmse([float(x) for x in test_data.values], forecast_ets), end="\t|\t")
    print(meanabs([float(x) for x in test_data.values], forecast_ets))

    print("\tARIMA", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in test_data.values], forecast_arima), end="\t|\t")
    print(meanabs([float(x) for x in test_data.values], forecast_arima))

    print("\tSeasonal Naive", end="\t\t\t|\t")
    print(rmse([float(x) for x in test_data.values], forecast_snaive), end="\t|\t")
    print(meanabs([float(x) for x in test_data.values], forecast_snaive))

    print("\tDrift", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in test_data.values], forecast_drift), end="\t|\t")
    print(meanabs([float(x) for x in test_data.values], forecast_drift))

    print("\tAverage", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in test_data.values], forecast_average), end="\t|\t")
    print(meanabs([float(x) for x in test_data.values], forecast_average))

if __name__ == "__main__":
    run()
