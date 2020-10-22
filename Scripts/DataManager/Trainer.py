import Scripts.Tools.eval as eval
import csv
import pickle
import pandas as pd
import xgboost as xgb
from Scripts.DataManager.BaseLines import average, seasonal_naive, drift
from pandas import DataFrame
from statsmodels.tools.eval_measures import rmse, meanabs
from statsmodels.tsa.api import ARIMA
from statsmodels.tsa.api import ExponentialSmoothing
import Scripts.DataManager.GSCV_tests as gst
import sys




def run(training_data: pd.DataFrame, validation_data: pd.DataFrame):

    #------------ Brute force tunning ----------------------
    pc = 0
    p_values = range(0, 3)
    d_values = range(0, 3)
    q_values = range(0, 10)
    best_score, best_cfg = float("inf"), None
    # for p in p_values:
    #     for d in d_values:
    #         for q in q_values:
    #             order = (p, d, q)
    #             try:
    #                 pc = pc + 1
    #                 mase = eval.mase(validation_data['adj close'].values, arima(training_data['adj close'], 120, order, training_data['ticker'][0], fit=True, save=False, load=False), 5)
    #                 if mase < best_score:
    #                     best_score, best_cfg = mase, order
    #                 print(('Teste %d - ARIMA%s MSE=%.3f' % (pc, order, mase)))
    #             except:
    #                 continue
    # print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
    #----------------------------------

    forecast_ets = ets(training_data['adj close'], 120, training_data['ticker'][0], fit=False, save=False, load=True)
    forecast_ets.index = validation_data.index
    forecast_arima = arima(training_data['adj close'], 120, best_cfg, training_data['ticker'][0], fit=False, save=False, load=True) # outros valores bons(1,0,1), (1,0,0), (2,0,1)
    forecast_arima.index = validation_data.index
    forecast_xgboost = xgboost(training_data, validation_data, ets=forecast_ets, arima=forecast_arima, fit=False, save=False, load=True)
    forecast_xgboost.index = validation_data.index
    forecast_snaive = seasonal_naive(training_data['adj close'], 5, 120)
    forecast_snaive.index = validation_data.index
    forecast_drift = drift(training_data['adj close'], 120)
    forecast_drift.index = validation_data.index
    forecast_average = average(training_data['adj close'], 120)
    forecast_average.index = validation_data.index

    result = pd.concat([forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average, validation_data['adj close']], axis=1, sort=False)
    result.columns = ['ETS', 'ARIMA', 'XGBoost', 'SNaive', 'Drift', 'Average', 'Real Values']

    print("Ação: " + str(training_data['ticker'][0]))
    eval_result = evaluation(validation_data['adj close'], forecast_ets, forecast_arima, forecast_xgboost, forecast_snaive, forecast_drift, forecast_average, verbose=True)

    save_result_stats(result, eval_result, training_data['ticker'][0])

def ets(time_serie, Npt, simple_ticker, fit: bool, save: bool, load: bool):
    filename = '../../Resources/TunnedModels/' + simple_ticker + '_ets_2020_07_31.pickle'
    if fit:
        ets_fit = ExponentialSmoothing(endog=time_serie.values.astype('float'), seasonal_periods=5, trend='mul', seasonal='add', damped=True).fit(use_brute=True)
        if save:
            # save the model to disk
            pickle.dump(ets_fit, open(filename, 'wb'))
    elif load:
        # load the model from disk
        ets_fit = pickle.load(open(filename, 'rb'))
    else:
        print("Error: fit and load parameters are both false.")
        sys.exit(-1)
    forecast_ets = [x for x in ets_fit.forecast(Npt)]
    return pd.Series(forecast_ets)

def arima(time_serie, Npt, order, simple_ticker, fit: bool, save: bool, load: bool):
    filename = '../../Resources/TunnedModels/' + simple_ticker + '_arima_2020_07_31.pickle'
    if fit:
        arima_fit = ARIMA(time_serie.values.astype('float'), order).fit(disp=False)
        if save:
            # save the model to disk
            pickle.dump(arima_fit, open(filename, 'wb'))
    elif load:
        # load the model from disk
        arima_fit = pickle.load(open(filename, 'rb'))
    else:
        print("Error: fit and load parameters are both false.")
        sys.exit(-1)
    forecast_arima = [x for x in arima_fit.forecast(Npt)[0]] # [0]= predições
    return pd.Series(forecast_arima)

def xgboost(training_data, validation_data, ets, arima, fit: bool, save: bool, load: bool):

    xgbr = xgb.XGBRegressor(objective ='reg:linear', verbosity=0)
    print(xgbr)

    tudo = pd.concat([training_data, validation_data])
    tudo['ets']= tudo['adj close']
    tudo['arima'] = tudo['adj close']
    tudo['ets'].loc[(len(tudo) - len(ets)):] = ets
    tudo['arima'].loc[(len(tudo) - len(arima)):] = arima
    tudo.drop(tudo.tail(120).index, inplace=True)

    training_data = tudo.drop(tudo.tail(120).index, inplace=False)
    validation_data = tudo.tail(120)

    train_target = training_data[['adj close']]
    train_features = training_data.drop(['adj close', 'ticker'], axis=1, inplace=False)
    test_features = validation_data.drop(['adj close', 'ticker'], axis=1, inplace=False)

    if fit:
        xgbr = gst.grid_xgboost(training_data, validation_data, 120, str(training_data['ticker'][0]), fit, save)
    elif load:
        filename = '../../Resources/TunnedModels/'+ training_data['ticker'][0] +'_xgboost_2020_07_31.pickle'
        xgbr = pickle.load(open(filename, 'rb'))
    else:
        print("Error: fit and load parameters are both false.")
        sys.exit(-1)

    forecast_xgboost = xgbr.predict(test_features)
    return pd.Series(data=forecast_xgboost, index=validation_data.index)

def evaluation(validation_data: pd.Series, forecast_ets: pd.Series, forecast_arima: pd.Series, forecast_xgboost: pd.Series, forecast_snaive: pd.Series, forecast_drift: pd.Series, forecast_average: pd.Series, verbose: bool):

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

    eval_results = DataFrame ([sn, df, av, xgb, ets, ar], index = ['seasonal_naive','drift','average','xgboost','ets','arima'],columns = ['RMSE','MAE','MASE', 'sMAPE'])
    return eval_results

def save_result_stats(forecasts: DataFrame, evaluations: DataFrame, ticker):
    eval_path = '../../Evaluations/'

    # Salva os dados em um arquivo .csv
    forecasts.to_csv(eval_path + ticker + '_2020_07_31' + '_forecasts.csv', mode='w', sep=';', na_rep='', header=True, index=True, date_format='%Y-%m-%d', decimal='.', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
    evaluations.to_csv(eval_path + ticker + '_2020_07_31' + '_evaluations.csv', mode='w', sep=';', na_rep='', header=True, index=True, date_format='%Y-%m-%d', decimal='.', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')