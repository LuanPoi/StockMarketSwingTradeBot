import pandas as pd
import numpy as np
import pandas_datareader as pdr
import yfinance as yf
import stockstats as ss
import datetime as dt
import csv
import statsmodels as sm
import statsmodels.tsa.api as smt


# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Informações iniciais                                           *
# ***************************************************************************************************************************************************************************************************************************************************************
print(
    "Configuracoes:\n"
    + "pdr: " + pdr.__version__ + "\n"
    + "pandas: " + pd.__version__ + "\n"
    + "numpy: " + np.__version__ + "\n"
    + "yfinance: " + yf.__version__ + "\n"
    + "statsmodels: " + sm.__version__ + "\n"
    #+ ": " +  + "\n"
)




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Inicializações                                                *
# ***************************************************************************************************************************************************************************************************************************************************************
caminho_datasets = "../Resources/Datasets/"
tickers = {
    "Inter": "BIDI4.SA",
    "Petrobras": "PETR4.SA",
    "Vale": "VALE3.SA",
    "Itau": "ITUB4.SA",
    "Ambev": "ABEV3.SA",
    "Sinqia": "SQIA3.SA",
    "Bovespa": "BOVA11.SA"
}




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Seleção                                                *
# ***************************************************************************************************************************************************************************************************************************************************************
ticker_selecionado = tickers['Petrobras']



'''
# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Aquisição                                                     *
# ***************************************************************************************************************************************************************************************************************************************************************
yf.pdr_override()
historico: pd.DataFrame = pdr.data.get_data_yahoo(ticker_selecionado, period="max")




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Data Cleansing                                                *
# ***************************************************************************************************************************************************************************************************************************************************************
# Remove linhas até achar a primeira segunda feira
toDrop = []
for x in range(historico.shape[0]):
    if historico.iloc[[x]].index.weekday == 0:
        break
    else:
        toDrop.append(x)
historico.drop(toDrop)

# Preenchimento de campos faltantes com estratégia custom
for i in range(historico.shape[0]):
    linha = historico.iloc[i]
    for coluna in range(len(linha.index)):
        if str(linha[coluna]) == str(np.nan):
            a_frente = 0
            valor = historico.iloc[i-1, coluna]
            while True:
                if i == 0:
                    a_frente = a_frente + 1
                    if str(historico.iloc[i + a_frente, coluna]) != str(np.nan):
                        valor = historico.iloc[i + a_frente, coluna]
                        for x in range(a_frente):
                            historico.iloc[i + x, coluna] = valor
                        a_frente = 0
                        valor = 0
                        break
                elif (i + a_frente + 1) == historico.shape[0]:
                    for x in range(a_frente):
                        historico.iloc[i + x, coluna] = historico.iloc[i-1, coluna]
                    a_frente = 0
                    valor = 0
                    break
                else:
                    a_frente = a_frente + 1
                    if str(historico.iloc[i + a_frente, coluna]) != str(np.nan):
                        valor = (historico.iloc[i + a_frente, coluna] - valor) / (1 + a_frente)
                        for x in range(a_frente):
                            historico.iloc[i + x, coluna] = ((1 + x) * valor) + historico.iloc[i-1, coluna]
                        a_frente = 0
                        valor = 0
                        break



# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Agregação e Pivotamento                                               *
# ***************************************************************************************************************************************************************************************************************************************************************
# TODO: Melhorar as features obtidas adicionando algumas mais úteis.
stock = ss.StockDataFrame.retype(historico)
data = {
    # volume delta against previous day
    'volume_delta': stock.get('volume_delta'),

    # open delta against next 2 day
    'open_2_d': stock.get('open_2_d'),

    # open price change (in percent)) between today and the day before yesterday
    # 'r' stands for rate.
    'open_-2_r': stock.get('open_-2_r'),

    # CR indicator, including 5, 10, 20 days moving average
    'cr': stock.get('cr'),
    'cr-ma1': stock.get('cr-ma1'),
    'cr-ma2': stock.get('cr-ma2'),
    'cr-ma3': stock.get('cr-ma3'),

    # KDJ, default to 9 days
    'kdjk': stock.get('kdjk'),
    'kdjd': stock.get('kdjd'),
    'kdjj': stock.get('kdjj'),

    # three days KDJK cross up 3 days KDJD
    # 'kdj_3_xu_kdjd_3': stock.get('kdj_3_xu_kdjd_3'),

    # 2 days simple moving average on open price
    'open_2_sma': stock.get('open_2_sma'),

    # MACD
    'macd': stock.get('macd'),
    # MACD signal line
    'macds': stock.get('macds'),
    # MACD histogram
    'macdh': stock.get('macdh'),

    # bolling, including upper band and lower band
    'boll': stock.get('boll'),
    'boll_ub': stock.get('boll_ub'),
    'boll_lb': stock.get('boll_lb'),

    # close price less than 10.0 in 5 days count
    'close_10.0_le_5_c': stock.get('close_10.0_le_5_c'),

    # CR MA2 cross up CR MA1 in 20 days count
    # 'cr-ma2_xu_cr-ma1_20_c': stock.get('cr-ma2_xu_cr-ma1_20_c'),

    # count forward(future)) where close price is larger than 10
    'close_10.0_ge_5_fc': stock.get('close_10.0_ge_5_fc'),

    # 6 days RSI
    'rsi_6': stock.get('rsi_6'),
    # 12 days RSI
    'rsi_12': stock.get('rsi_12'),

    # 10 days WR
    'wr_10': stock.get('wr_10'),
    # 6 days WR
    'wr_6': stock.get('wr_6'),

    # CCI, default to 14 days
    'cci': stock.get('cci'),
    # 20 days CCI
    'cci_20': stock.get('cci_20'),

    # TR (true range))
    'tr': stock.get('tr'),
    # ATR (Average True Range))
    'atr': stock.get('atr'),

    # DMA, difference of 10 and 50 moving average
    'dma': stock.get('dma'),

    # DMI
    # +DI, default to 14 days
    'pdi': stock.get('pdi'),
    # -DI, default to 14 days
    'mdi': stock.get('mdi'),
    # DX, default to 14 days of +DI and -DI
    'dx': stock.get('dx'),
    # ADX, 6 days SMA of DX, same as '': stock.get('dx_6_ema'))
    'adx': stock.get('adx'),
    # ADXR, 6 days SMA of ADX, same as '': stock.get('adx_6_ema'))
    'adxr': stock.get('adxr'),

    # TRIX, default to 12 days
    'trix': stock.get('trix'),
    # TRIX based on the close price for a window of 3
    'close_3_trix': stock.get('close_3_trix'),
    # MATRIX is the simple moving average of TRIX
    'trix_9_sma': stock.get('trix_9_sma'),
    # TEMA, another implementation for triple ema
    'tema': stock.get('tema'),
    # TEMA based on the close price for a window of 2
    'close_2_tema': stock.get('close_2_tema'),

    # VR, default to 26 days
    'vr': stock.get('vr'),
    # MAVR is the simple moving average of VR
    'vr_6_sma': stock.get('vr_6_sma')
}
stats = pd.DataFrame(data)

# Concatenação das features com os dados originais
historico = pd.concat([historico, stats], axis=1, sort=False)




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Salvamento e Carregamento da base                                               *
# ***************************************************************************************************************************************************************************************************************************************************************
# Salva o dataframe em "<ticker>.csv" e os dtypes de cada coluna em "<ticker>_metadata.csv"
historico.to_csv(caminho_datasets+ticker_selecionado+'.csv', mode='a', sep=';', na_rep='', header=True, index=True, date_format='%Y-%m-%d', decimal='.', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
historico.dtypes.to_csv(caminho_datasets+ticker_selecionado+'_metadata'+'.csv', mode='w', sep=';', header=False, index=True, quotechar='"', encoding='utf-8')

historico = None
'''
# Carrega o dataframe e os dtypes dos arquivos .csv
ticker_metadata = pd.read_csv(caminho_datasets+ticker_selecionado+'_metadata'+'.csv', sep=';', quotechar='"', names=['dtypes'], index_col=0).to_dict()['dtypes']
historico = pd.read_csv(caminho_datasets+ticker_selecionado+'.csv', sep=';', header=0, index_col=0, quoting=csv.QUOTE_NONNUMERIC, dtype=ticker_metadata)
# Formata o index para datetime
historico.index = pd.to_datetime(historico.index)




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Pré treinamento                                               *
# ***************************************************************************************************************************************************************************************************************************************************************
# Faz o corte na data limite
historico.drop(historico[historico.index > dt.datetime(2020,7,31)].index, inplace=True)
# Faz o shift de 120 dias da coluna alvo
colunasShift = ['adj close']
for item in colunasShift:
    historico[item] = historico[item].shift(-120, fill_value=np.nan)
# Corta os 120 dias de sobra
historico.drop(historico.tail(120).index, inplace=True)
# TODO: Colocar as 'lag features' em escala




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - Separação Treino e Validação                                               *
# ***************************************************************************************************************************************************************************************************************************************************************
# Separação em conjuntos treino e validação
treino = historico.drop(historico.tail(120).index, inplace=False)
validacao = historico.tail(120)




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico - ETS                                               *
# ***************************************************************************************************************************************************************************************************************************************************************
ets_pesos = smt.ExponentialSmoothing(endog=treino['adj close'], seasonal_periods=5, trend='mul', seasonal='add', damped_trend=True).fit(use_brute=True)
ets_previsao = pd.Series([x for x in ets_pesos.forecast(120)], index=validacao.index)




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico -                                                *
# ***************************************************************************************************************************************************************************************************************************************************************
arima_pesos = smt.arima.ARIMA(endog=treino['adj close'], order=(1, 1, 1)).fit()
temp = arima_pesos.forecast(120)
forecast_previsao = pd.Series([x for x in arima_pesos.forecast(120)], index=validacao.index) # [0]= predições




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico -                                                *
# ***************************************************************************************************************************************************************************************************************************************************************




# ***************************************************************************************************************************************************************************************************************************************************************
# *                              Tópico -                                                *
# ***************************************************************************************************************************************************************************************************************************************************************

print('\nfim')
