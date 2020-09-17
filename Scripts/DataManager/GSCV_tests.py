
import xgboost as xgb
import numpy as np
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.api import ARIMA
from sklearn.model_selection import GridSearchCV
import sklearn

metricas = ['explained_variance', 'max_error', 'neg_mean_absolute_error', 'neg_mean_squared_error', 'neg_root_mean_squared_error', 'neg_mean_squared_log_error', 'neg_median_absolute_error', 'r2', 'neg_mean_poisson_deviance', 'neg_mean_gamma_deviance']

def grid_xgboost(training_data, validation_data, Npt):
    xgbr = xgb.XGBRegressor()

    hyper = {
        'objective': ['reg:linear', 'reg:squarederror'],
        'booster': ['gblinear'],
        #'colsample_bylevel': np.linspace(0., 1., 10),
        'colsample_bynode': np.linspace(0., 1., 10),
        #'colsample_bytree': np.linspace(0., 1., 10),
        #'gamma': np.linspace(0., 10., 5),
        #'gpu_id': [], #instalar o cuda e o xgboost-gpu
        #'importance_type': ['gain', 'weight', 'cover', 'total_gain' or 'total_cover'],
        'learning_rate': [0.01, 0.1, 0.05],
        #'max_delta_step': np.arange(10),
        'max_depth': np.arange(10),
        #'min_child_weight': np.linspace(0., 10., 5),
        'n_estimators': np.arange(10),
        'n_jobs': [4],
        #'num_parallel_tree': np.arange(10),
        'reg_alpha': np.linspace(0., 1., 10),
        'reg_lambda': np.linspace(0., 1., 10),
        #'scale_pos_weight': np.linspace(0., 1., 2),
        'subsample': np.linspace(0., 1., 10),
        'tree_method': ['exact'],
        'validate_parameters': [True],
        'verbosity': [0]
    }

    train_target = training_data[['adj close']]
    train_features = training_data.drop(['adj close', 'ticker'], axis=1, inplace=False)
    test_features = validation_data.drop(['adj close', 'ticker'], axis=1, inplace=False)

    grid = GridSearchCV(xgbr, param_grid=hyper, scoring=metricas, verbose=100, refit='neg_root_mean_squared_error', return_train_score=False)
    grid.fit(X=train_features, y=train_target)
    print(grid.best_estimator_)
    pd.set_option('max_columns', 200)
    print(pd.DataFrame(grid.cv_results_))

    print("\n\n\n------------------- Fim -------------------\n\n\n")
    # forecast_xgboost = xgbr.predict(test_features)
    # return pd.Series(data=forecast_xgboost, index=validation_data['Date'])