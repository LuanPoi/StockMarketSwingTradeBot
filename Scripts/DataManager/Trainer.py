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
import Scripts.Tools.eval as eval
from sklearn.model_selection import GridSearchCV

import Scripts.DataManager.GSCV_tests as gst

def ets(time_serie, Npt):
    #TODO: Fazer retornar os dados na forma de um pandas.Series
    ets_fit = ExponentialSmoothing(time_serie.values, seasonal_periods=5, trend='add', seasonal='add', damped=True).fit()
    forecast_ets = [x for x in ets_fit.forecast(Npt)]
    return forecast_ets

def arima(time_serie, Npt):
    # TODO: Fazer retornar os dados na forma de um pandas.Series
    arima_fit = ARIMA(time_serie.values, (1, 1, 1)).fit(disp=False)
    forecast_arima = [x for x in arima_fit.forecast(Npt)[0]] # [0]= predições
    return forecast_arima

#XGB_Regressor
def xgboost(training_data, validation_data, Npt):
    # Warning: o XGBoost precisa receber as features do conjunto de validação mas você só consegue estes dados já tendo os dados da previsão.

    xgbr = xgb.XGBRegressor(objective ='reg:linear', verbosity=0)
    print(xgbr)
    train_target = training_data[['adj close']]
    train_features = training_data.drop(['adj close', 'Date', 'ticker'], axis=1, inplace=False)
    test_features = validation_data.drop(['adj close', 'Date', 'ticker'], axis=1, inplace=False)
    xgbr.fit(X=train_features, y=train_target, verbose=True)
    forecast_xgboost = xgbr.predict(test_features)
    return pd.Series(data=forecast_xgboost, index=validation_data['Date'])

def debug(validation_data: pd.Series,
          forecast_ets: pd.Series,
          forecast_arima: pd.Series,
          forecast_xgboost: pd.DataFrame,
          forecast_snaive: pd.Series,
          forecast_drift: pd.Series,
          forecast_average: pd.Series):

    print("\tPrediction model\t\t|\tRMSE\t\t\t\t|\tMAE\t\t\t\t\t|\tSeasonal MASE\t\t|\tSMAPE")
    print("\t-------------------------------------------------------------------------------------------------")

    print("\tXGBoost Regression", end="\t\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_xgboost), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_xgboost), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_xgboost, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_xgboost))

    print("\tExponentialSmoothing", end="\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_ets), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_ets), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_ets, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_ets))

    print("\tARIMA", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_arima), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_arima), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_arima, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_arima))

    print("\tSeasonal Naive", end="\t\t\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_snaive), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_snaive), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_snaive, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_snaive))

    print("\tDrift", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_drift), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_drift), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_drift, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_drift))

    print("\tAverage", end="\t\t\t\t\t|\t")
    print(rmse([float(x) for x in validation_data.values], forecast_average), end="\t|\t")
    print(meanabs([float(x) for x in validation_data.values], forecast_average), end="\t|\t")
    print(eval.mase(validation_data.values, forecast_average, 5), end="\t|\t")
    print(eval.smape(validation_data.values, forecast_average))

def run(training_data: pd.DataFrame, validation_data: pd.DataFrame):

    training_data_serie = pd.Series(
                    data = training_data['adj close'],
                    index = training_data.index
    )
    test_data_serie = pd.Series(
                    data = validation_data['adj close'],
                    index = validation_data.index
    )

    # debug(
    #     validation_data= test_data_serie,
    #     forecast_ets= ets(training_data_serie, 120),
    #     forecast_arima= arima(training_data_serie, 120),
    #     forecast_xgboost= xgboost(training_data, validation_data, 120),
    #     forecast_snaive= seasonal_naive(training_data_serie, 5, 120),
    #     forecast_drift= drift(training_data_serie, 120),
    #     forecast_average= average(training_data_serie, 120)
    # )

    gst.grid_xgboost(training_data, validation_data, 120)