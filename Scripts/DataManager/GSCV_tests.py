
import xgboost as xgb
import numpy as np
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.api import ARIMA
from sklearn.model_selection import GridSearchCV
import pickle
import sklearn

metricas = ['max_error', 'neg_mean_absolute_error', 'neg_mean_squared_error', 'neg_root_mean_squared_error', 'neg_median_absolute_error']

def grid_xgboost(training_data, validation_data, Npt, simple_ticker):
    xgbr = xgb.XGBRegressor()

    hyper = {
        'objective': [ 'reg:linear', 'reg:squarederror'],
        'booster': ['gblinear'],
        #'colsample_bylevel': np.linspace(0., 1., 10),
        'colsample_bynode': [0.3, 0.5, 0.7, 0.8, 1],
        #'colsample_bytree': np.linspace(0., 1., 10),
        #'gamma': np.linspace(0., 10., 5),
        #'importance_type': ['gain', 'weight', 'cover', 'total_gain' or 'total_cover'],
        'learning_rate': [0.01, 0.05, 0.1, 0.5, 0.75, 1],
        #'max_delta_step': np.arange(10),
        'max_depth': [3, 4, 5, 6, 7, 8],
        #'min_child_weight': np.linspace(0., 10., 5),
        'n_estimators': [50, 100, 150],
        #'num_parallel_tree': np.arange(10),
        #'reg_alpha': np.linspace(0., 1., 7),
        #'reg_lambda': np.linspace(0., 1., 8),
        #'scale_pos_weight': np.linspace(0., 1., 2),
        'subsample': [0.8, 1],
        'tree_method': ['gpu_hist'],
        'gpu_id': [0],
        'validate_parameters': [True],
        'verbosity': [0]
    }

    train_target = training_data[['adj close']]
    train_features = training_data.drop(['adj close', 'ticker'], axis=1, inplace=False)
    test_features = validation_data.drop(['adj close', 'ticker'], axis=1, inplace=False)

    grid = GridSearchCV(xgbr, param_grid=hyper, scoring=metricas, verbose=1, refit='neg_root_mean_squared_error', return_train_score=False, n_jobs=-1)
    grid.fit(X=train_features.astype('float'), y=train_target.astype('float'))

    # save the model to disk
    filename = '../../Resources/TunnedModels/'+simple_ticker+'_xgboost_2020_07_31.pickle'
    pickle.dump(grid.best_estimator_, open(filename, 'wb'))

    print("----------------best estimator-------------------")
    print(pd.DataFrame(grid.cv_results_))
    print("----------------best estimator-------------------")
    return