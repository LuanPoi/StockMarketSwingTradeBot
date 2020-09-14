import numpy as np
import pandas as pd

EPSILON = 1e-10

# TODO: sMASE (seasonal Mean Absolute Scaled Erro
def mase(test_data: pd.Series, forecast_data: pd.Series, season_range: int = 1):
    """
    Mean Absolute Scaled Error
    Baseline (benchmark) is computed with naive forecasting (shifted by @seasonality)
    """
    return mae(test_data, forecast_data) / mae(test_data[season_range:], _naive_forecasting(test_data, season_range))

def mae(test_data: pd.Series, forecast_data: pd.Series):
    """ Mean Absolute Error """
    return np.mean(np.abs(_error(test_data, forecast_data)))

def _naive_forecasting(test_data: pd.Series, season_range: int = 1):
    """ Naive forecasting method which just repeats previous samples """
    return test_data[:-season_range]

def _error(test_data: pd.Series, forecast_data: pd.Series):
    """ Simple error """
    return test_data - forecast_data

def smape(test_data: np.ndarray, forecast_data: np.ndarray):
    """
    Symmetric Median Absolute Percentage Error
    Note: result is NOT multiplied by 100
    """
    return np.median(2.0 * np.abs(test_data - forecast_data) / ((np.abs(test_data) + np.abs(forecast_data)) + EPSILON))