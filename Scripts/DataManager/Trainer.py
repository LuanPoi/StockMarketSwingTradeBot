from Scripts.DataManager.BaseLines import average, seasonal_naive, drift
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.api import ARIMA
from statsmodels.tools.eval_measures import rmse, meanabs
from pandas import DataFrame
import xgboost as xgb
import numpy as np
import pandas as pd
import Scripts.Tools.eval as eval
import plotly.offline as py
import plotly.graph_objs as go

import pickle

def run(training_data: pd.DataFrame, validation_data: pd.DataFrame):
    training_data_serie = pd.Series(
                    data = training_data['adj close'],
                    index = training_data.index
    )
    test_data_serie = pd.Series(
                    data = validation_data['adj close'],
                    index = validation_data.index
    )

    forecast_ets = ets(training_data_serie, 120)
    forecast_arima = arima(training_data_serie, 120)
    forecast_xgboost = xgboost(training_data, test_data_serie, ets=forecast_ets, arima=forecast_arima)
    forecast_snaive = seasonal_naive(training_data_serie, 5, 120)
    forecast_drift = drift(training_data_serie, 120)
    forecast_average = average(training_data_serie, 120)

    plot_graph(forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average, test_data_serie)

    debug(test_data_serie, forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average, verbose=True)

def ets(time_serie, Npt):
    #TODO: Fazer retornar os dados na forma de um pandas.Series
    ets_fit = ExponentialSmoothing(endog=time_serie.values, seasonal_periods=5, trend='mul', seasonal='add', damped=True).fit()
    forecast_ets = [x for x in ets_fit.forecast(Npt)]
    return pd.Series(forecast_ets)

def arima(time_serie, Npt):
    # TODO: Fazer retornar os dados na forma de um pandas.Series
    arima_fit = ARIMA(time_serie.values, (0, 0, 1)).fit(disp=False)
    forecast_arima = [x for x in arima_fit.forecast(Npt)[0]] # [0]= predições
    return pd.Series(forecast_arima)

def xgboost(training_data, validation_data, ets, arima):

    xgbr = xgb.XGBRegressor(objective ='reg:linear', verbosity=0)
    print(xgbr)

    tudo = pd.concat([training_data, validation_data])
    tudo['ets']= tudo['adj close']
    tudo['arima'] = tudo['adj close']
    tudo['ets'].loc[(len(tudo) - len(ets)):] = ets
    tudo['arima'].loc[(len(tudo) - len(arima)):] = arima

    colunasShift = ['adj close','ets', 'arima']
    for item in colunasShift:
        tudo[item] = tudo[item].shift(-120, fill_value=np.nan)

    tudo.drop(tudo.tail(120).index, inplace=True)

    training_data = tudo.drop(tudo.tail(120).index, inplace=False)
    validation_data = tudo.tail(120)

    train_target = training_data[['adj close']]
    train_features = training_data.drop(['adj close', 'ticker'], axis=1, inplace=False)
    test_features = validation_data.drop(['adj close', 'ticker'], axis=1, inplace=False)

    #return gst.grid_xgboost(training_data, validation_data, 120, str(training_data['ticker'][0]))

    filename = '../../Resources/TunnedModels/'+ training_data['ticker'][0][:-3] +'_xgboost_31_07_covid.tmsave'
    xgbr = pickle.load(open(filename, 'rb'))

    forecast_xgboost = xgbr.predict(test_features)
    return pd.Series(data=forecast_xgboost, index=validation_data.index)

def debug(validation_data: pd.Series, forecast_ets: pd.Series, forecast_arima: pd.Series, forecast_xgboost: pd.DataFrame, forecast_snaive: pd.Series, forecast_drift: pd.Series, forecast_average: pd.Series, verbose: bool):

    print("\tPrediction model\t\t|\tRMSE\t\t\t\t|\tMAE\t\t\t\t\t|\tSeasonal MASE\t\t|\tSMAPE")
    print("\t-------------------------------------------------------------------------------------------------")

    sn = [
        rmse([float(x) for x in validation_data.values], forecast_snaive),
        meanabs([float(x) for x in validation_data.values], forecast_snaive),
        eval.mase(validation_data.values, forecast_snaive, 5),
        eval.smape(validation_data.values, forecast_snaive)
    ]
    if verbose:
        print("\tSeasonal Naive", end="\t\t\t|\t")
        print(sn[0], end="\t|\t")
        print(sn[1], end="\t|\t")
        print(sn[2], end="\t|\t")
        print(sn[3])

    df = [
        rmse([float(x) for x in validation_data.values], forecast_drift),
        meanabs([float(x) for x in validation_data.values], forecast_drift),
        eval.mase(validation_data.values, forecast_drift, 5),
        eval.smape(validation_data.values, forecast_drift)
    ]
    if verbose:
        print("\tDrift", end="\t\t\t\t\t|\t")
        print(df[0], end="\t|\t")
        print(df[1], end="\t|\t")
        print(df[2], end="\t|\t")
        print(df[3])
    av = [
        rmse([float(x) for x in validation_data.values], forecast_average),
        meanabs([float(x) for x in validation_data.values], forecast_average),
        eval.mase(validation_data.values, forecast_average, 5),
        eval.smape(validation_data.values, forecast_average)
    ]
    if verbose:
        print("\tAverage", end="\t\t\t\t\t|\t")
        print(av[0], end="\t|\t")
        print(av[1], end="\t|\t")
        print(av[2], end="\t|\t")
        print(av[3])

    xgb = [
        rmse([float(x) for x in validation_data.values], forecast_xgboost),
        meanabs([float(x) for x in validation_data.values], forecast_xgboost),
        eval.mase(validation_data.values, forecast_xgboost, 5),
        eval.smape(validation_data.values, forecast_xgboost)
    ]
    if verbose:
        print("\tXGBoost Regression", end="\t\t|\t")
        print(xgb[0], end="\t|\t")
        print(xgb[1], end="\t|\t")
        print(xgb[2], end="\t|\t")
        print(xgb[3])

    ets = [
        rmse([float(x) for x in validation_data.values], forecast_ets),
        meanabs([float(x) for x in validation_data.values], forecast_ets),
        eval.mase(validation_data.values, forecast_ets, 5),
        eval.smape(validation_data.values, forecast_ets)
    ]
    if verbose:
        print("\tExponentialSmoothing", end="\t|\t")
        print(ets[0], end="\t|\t")
        print(ets[1], end="\t|\t")
        print(ets[2], end="\t|\t")
        print(ets[3])

    ar = [
        rmse([float(x) for x in validation_data.values], forecast_arima),
        meanabs([float(x) for x in validation_data.values], forecast_arima),
        eval.mase(validation_data.values, forecast_arima, 5),
        eval.smape(validation_data.values, forecast_arima)
    ]
    if verbose:
        print("\tARIMA", end="\t\t\t\t\t|\t")
        print(ar[0], end="\t|\t")
        print(ar[1], end="\t|\t")
        print(ar[2], end="\t|\t")
        print(ar[3])

    result = DataFrame ([sn, df, av, xgb, ets, ar], index = ['seasonal_naive','drift','average','xgboost','ets','arima'],columns = ['RMSE','MAE','MASE', 'sMAPE'])
    return result

def plot_graph(forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average, test_data_serie):
    # Gráfico usando apenas marcadores
    trace1 = go.Scatter(x=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y=[10, 9, 11, 8, 12],
                        mode='lines',
                        name='Gráfico com linhas tracejadas',
                        line={'color': '#ee5253',
                              'dash': 'dash'})