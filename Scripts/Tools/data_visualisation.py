import matplotlib.pyplot as plt
import pandas as pd
import csv


tickers = {
        "Inter": "BIDI4.SA",
        "Petrobras": "PETR4.SA",
        "Vale": "VALE3.SA",
        "Itau": "ITUB4.SA",
        "Ambev": "ABEV3.SA",
        "Sinqia": "SQIA3.SA",
        "Bovespa": "BOVA11.SA"
}
for ticker in tickers.values():
    eval_path = '../../Evaluations/'

    forecasts = pd.read_csv(eval_path + ticker + '_2020_07_31' + '_forecasts.csv', sep=';', decimal='.', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')

    # gca stands for 'get current axis'
    ax = plt.gca()

    ax.set(xlabel='Data', ylabel='Preço (R$)',
           title='Previsão do valor da ação \"' + ticker[:-3] + '\"')

    forecasts['Real Values'].plot(kind='line', y='Real Values', color='black', ax=ax)
    forecasts['ETS'].plot(kind='line', y='ETS', color='red', ax=ax)
    forecasts['ARIMA'].plot(kind='line', y='ARIMA', color='green', ax=ax)
    forecasts['XGBoost'].plot(kind='line', y='XGBoost', color='blue', ax=ax)
    forecasts['SNaive'].plot(kind='line', y='SNaive', color='purple', ax=ax)
    forecasts['Drift'].plot(kind='line', y='Drift', color='pink', ax=ax)
    forecasts['Average'].plot(kind='line', y='Average', color='brown', ax=ax)

    plt.show()