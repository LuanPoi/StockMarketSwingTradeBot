from Scripts.DataManager.MySQLManager import MySQLManager
from Scripts.DataManager.YahooAPIHandler import YahooAPIHandler

# # * colocar essas funções na main quando quiser inserir novas ações
# dataFrame = yahooAPIHandler.historical(currentTicker, None, None)
# mySQLManager.create("stock", currentTicker, dataFrame, True)

import sys
sys.setrecursionlimit(30000)

from datetime import datetime
import math
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

def SES(DataFrame):
    fit1 = SimpleExpSmoothing(DataFrame).fit(smoothing_level=0.2, optimized=False)
    fcast1 = fit1.forecast(3).rename(r'$\alpha=0.2$')
    fit2 = SimpleExpSmoothing(DataFrame).fit(smoothing_level=0.6, optimized=False)
    fcast2 = fit2.forecast(3).rename(r'$\alpha=0.6$')
    fit3 = SimpleExpSmoothing(DataFrame).fit()
    fcast3 = fit3.forecast(3).rename(r'$\alpha=%s$' % fit3.model.params['smoothing_level'])

    ax = DataFrame.plot(marker='o', color='black', figsize=(12, 8))
    fcast1.plot(marker='o', ax=ax, color='blue', legend=True)
    fit1.fittedvalues.plot(marker='o', ax=ax, color='blue')
    fcast2.plot(marker='o', ax=ax, color='red', legend=True)

    fit2.fittedvalues.plot(marker='o', ax=ax, color='red')
    fcast3.plot(marker='o', ax=ax, color='green', legend=True)
    fit3.fittedvalues.plot(marker='o', ax=ax, color='green')
    plt.show()

def Holt(DataFrame):
    fit1 = Holt(DataFrame).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
    fcast1 = fit1.forecast(5).rename("Holt's linear trend")
    # fit2 = Holt(DataFrame, exponential=True).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
    # fcast2 = fit2.forecast(5).rename("Exponential trend")
    # fit3 = Holt(DataFrame, damped=True).fit(smoothing_level=0.8, smoothing_slope=0.2)
    # fcast3 = fit3.forecast(5).rename("Additive damped trend")
    #
    ax = DataFrame.plot(color="black", marker="o", figsize=(12, 8))
    fit1.fittedvalues.plot(ax=ax, color='blue')
    fcast1.plot(ax=ax, color='blue', marker="o", legend=True)
    # fit2.fittedvalues.plot(ax=ax, color='red')
    # fcast2.plot(ax=ax, color='red', marker="o", legend=True)
    # fit3.fittedvalues.plot(ax=ax, color='green')
    # fcast3.plot(ax=ax, color='green', marker="o", legend=True)

    plt.show()

def Holt_Winters(DataFrame):
    fit1 = ExponentialSmoothing(DataFrame, seasonal_periods=5, trend='add', seasonal='add').fit(use_boxcox=False)
    fit2 = ExponentialSmoothing(DataFrame, seasonal_periods=5, trend='add', seasonal='mul').fit(use_boxcox=False)
    fit3 = ExponentialSmoothing(DataFrame, seasonal_periods=5, trend='add', seasonal='add', damped=True).fit(use_boxcox=False)
    fit4 = ExponentialSmoothing(DataFrame, seasonal_periods=5, trend='add', seasonal='mul', damped=True).fit(use_boxcox=False)
    results = pd.DataFrame(index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$\gamma$", r"$l_0$", "$b_0$", "SSE"])
    params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'smoothing_seasonal', 'initial_level',
              'initial_slope']
    results["Additive"] = [fit1.params[p] for p in params] + [fit1.sse]
    results["Multiplicative"] = [fit2.params[p] for p in params] + [fit2.sse]
    results["Additive Dam"] = [fit3.params[p] for p in params] + [fit3.sse]
    results["Multiplica Dam"] = [fit4.params[p] for p in params] + [fit4.sse]

    ax = DataFrame.plot(figsize=(10, 6), marker='o', color='black', title="Forecasts from Holt-Winters' multiplicative method")
    ax.set_ylabel("Stock price (R$)")
    ax.set_xlabel("Date")
    fit1.fittedvalues.plot(ax=ax, style='--', color='red')
    fit2.fittedvalues.plot(ax=ax, style='--', color='green')

    fit1.forecast(8).rename('Holt-Winters (add-add-seasonal)').plot(ax=ax, style='--', marker='o', color='red',
                                                                    legend=True)
    fit2.forecast(8).rename('Holt-Winters (add-mul-seasonal)').plot(ax=ax, style='--', marker='o', color='green',
                                                                    legend=True)

    #plt.show()
    #print(results)
    #df = pd.DataFrame(np.c_[DataFrame, fit1.level, fit1.slope, fit1.season, fit1.fittedvalues],
    #                  columns=[r'$y_t$', r'$l_t$', r'$b_t$', r'$s_t$', r'$\hat{y}_t$'], index=DataFrame.index)
    #df.append(fit1.forecast(8).rename(r'$\hat{y}_t$').to_frame(), sort=True)
    #print(df)

    states1 = pd.DataFrame(np.c_[fit1.level, fit1.slope, fit1.season], columns=['level', 'slope', 'seasonal'],
                           index=DataFrame.index)
    states2 = pd.DataFrame(np.c_[fit2.level, fit2.slope, fit2.season], columns=['level', 'slope', 'seasonal'],
                           index=DataFrame.index)
    fig, [[ax1, ax4], [ax2, ax5], [ax3, ax6]] = plt.subplots(3, 2, figsize=(12, 8))
    states1[['level']].plot(ax=ax1)
    states1[['slope']].plot(ax=ax2)
    states1[['seasonal']].plot(ax=ax3)
    states2[['level']].plot(ax=ax4)
    states2[['slope']].plot(ax=ax5)
    states2[['seasonal']].plot(ax=ax6)
    plt.show()


def printagrafico(data, ticker):
    # Plot the adjusted close price
    data['Close'].plot(figsize=(10, 7))
    # Define the label for the title of the figure
    plt.title("Adjusted Close Price of %s" % ticker, fontsize=16)
    # Define the labels for x-axis and y-axis
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    # Plot the grid lines
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    # Show the plot
    plt.show()
