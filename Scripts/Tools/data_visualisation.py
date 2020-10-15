import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

    evaluations = pd.read_csv(eval_path + ticker + '_2019_12_31' + '_evaluations.csv', sep=';', decimal='.', header=0, index_col=0, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')

    indexes = ['seasonal_naive', 'drift', 'average']

    columns = ['RMSE', 'MAE', 'MASE']

    rmse = ['', np.inf]
    mae = ['', np.inf]
    mase = ['', np.inf]


    for algo in indexes:
        if evaluations.loc[algo, 'RMSE'] < rmse[1]:
            rmse[0] = algo;
            rmse[1] = evaluations.loc[algo, 'RMSE']

        if evaluations.loc[algo, 'MAE'] < mae[1]:
            mae[0] = algo;
            mae[1] = evaluations.loc[algo, 'MAE']

        if evaluations.loc[algo, 'MASE'] < mae[1]:
            mase[0] = algo;
            mase[1] = evaluations.loc[algo, 'MASE']

    best_baseline = ['', -1]
    for algo in indexes:
        counter = 0
        if rmse[0] == algo:
            counter = counter + 1
        if mae[0] == algo:
            counter = counter + 1
        if mase[0] == algo:
            counter = counter + 1
        if counter > best_baseline[1]:
            best_baseline = [algo, counter]

    evaluations.drop('sMAPE', axis=1, inplace=False).transpose().plot.bar()
    plt.title('Erro dos modelos na previsão da ação \"' + ticker + '\" durante a COVID-19')
    plt.xlabel('Métrica de avaliação')
    plt.ylabel('Erro')
    plt.show()


    evaluations['sMAPE'].apply(lambda x: x * 100).transpose().plot.bar()
    plt.title('Erro percentual (%) dos modelos na previsão da ação \"' + ticker + '\" durante a COVID-19')
    plt.xlabel('Métrica de avaliação')
    plt.ylabel('Erro percentual (%)')
    plt.show()

    print(best_baseline[0] + " é o melhor.")

    if best_baseline[0] == 'average':
        best_baseline[0] = 'Average'
    if best_baseline[0] == 'drift':
        best_baseline[0] = 'Drift'
    if best_baseline[0] == 'seasonal_naive':
        best_baseline[0] = 'SNaive'

    toDrop = ['SNaive', 'Drift', 'Average']
    toDrop.remove(best_baseline[0])



    forecasts = pd.read_csv(eval_path + ticker + '_2019_12_31' + '_forecasts.csv', sep=';', decimal='.', header=0, index_col=0, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
    forecasts.drop(toDrop, axis=1, inplace=True)



    forecasts.plot()
    plt.title('Previsões feitas para a ação \"' + ticker + '\" durante a COVID-19')
    plt.xlabel('Dias')
    plt.ylabel('Preço da ação (R$)')

    # # gca stands for 'get current axis'
    # ax = plt.gca()
    #
    # ax.set(xlabel='Data', ylabel='Preço (R$)',
    #        title='Previsão do valor da ação \"' + ticker[:-3] + '\"')
    #
    # forecasts['Real Values'].plot(kind='line', y='Real Values', color='black', ax=ax)
    # forecasts['ETS'].plot(kind='line', y='ETS', color='red', ax=ax)
    # forecasts['ARIMA'].plot(kind='line', y='ARIMA', color='green', ax=ax)
    # forecasts['XGBoost'].plot(kind='line', y='XGBoost', color='blue', ax=ax)
    # forecasts['SNaive'].plot(kind='line', y='SNaive', color='purple', ax=ax)
    # forecasts['Drift'].plot(kind='line', y='Drift', color='pink', ax=ax)
    # forecasts['Average'].plot(kind='line', y='Average', color='brown', ax=ax)

    plt.show()