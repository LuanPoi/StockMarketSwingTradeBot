import  Scripts.DataManager.Trainer as Trainer
import  Scripts.DataManager.MySQLManager as MSQLM
import Scripts.DataManager.YahooAPIHandler as YAPIH

from datetime import datetime
import pandas as pd
import numpy as np
from stockstats import StockDataFrame

tickers = {
        "Inter": "BIDI4.SA",
        "Petrobras": "PETR4.SA",
        "Vale": "VALE3.SA",
        "Itau": "ITUB4.SA",
        "Ambev": "ABEV3.SA",
        "Sinqia": "SQIA3.SA",
        "Bovespa": "BOVA11.SA"
}

def run():
    dataset_base_path = "../../Resources/Datasets/"
    # Popula o csv com os dados de todas as ações de uma vez
    # populate_csv(tickers, dataset_base_path)

    # # Carrega os dados de uma determinada ação do banco de dados
    # mySQLManager = MSQLM.MySQLManager("localhost", "root", "toor")
    # mySQLManager.connect('stock_market')
    # data = mySQLManager.read('select * from stock where ticker=\'' + tickers['Itau'] + '\'')

    # Carrega os dados de todas as ações de um arquivo CSV e joga fora aquelas com ticker diferente do escolhido
    data = pd.read_csv(dataset_base_path+'stock.csv')
    data.drop(data[data['ticker'] != tickers['Petrobras']].index, inplace=True)

    #Separa os dados entre treinamento e validação (dentro da data limite usada no documento)
    training_data = data.drop(data.tail(120).index, inplace=False)
    validation_data = data.tail(120)

    training_data.set_index('Date', inplace=True)
    validation_data.set_index('Date', inplace=True)

    Trainer.run(training_data, validation_data)

def populate_mysql(tickers: dict):

    toggle = True

    for ticker in tickers.values():
        raw_data = YAPIH.historical(str(ticker))
        if toggle:
            ticker_serie = pd.Series([str(ticker) for x in range(len(raw_data))], raw_data.index, name="ticker")
            processed_data = pd.concat([ticker_serie, raw_data, stock_stats(raw_data)], axis=1, sort=False)

            processed_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            processed_data['adj close'] = processed_data['adj close'].replace(np.nan, value=processed_data['adj close'].mean(), inplace=False)

            training_data = processed_data.drop(processed_data[processed_data.index > datetime(2020,7,31)].index, inplace=False)
            test_data = processed_data.drop(processed_data[processed_data.index <= datetime(2020,7,31)].index, inplace=False)

            mySQLManager = MSQLM.MySQLManager("localhost", "root", "toor")
            mySQLManager.connect('stock_market')
            mySQLManager.create('stock', training_data, 'replace')
            mySQLManager.connect('stock_market')
            mySQLManager.create('stock_test', test_data, 'replace')
            toggle = False
        else:
            ticker_serie = pd.Series([str(ticker) for x in range(len(raw_data))], raw_data.index, name="ticker")
            processed_data = pd.concat([ticker_serie, raw_data, stock_stats(raw_data)], axis=1, sort=False)

            processed_data.replace([np.inf, -np.inf], np.nan)
            processed_data['adj close'] = processed_data['adj close'].replace(np.nan, value=processed_data['adj close'].mean(), inplace=False)

            training_data = processed_data.drop(processed_data[processed_data.index > datetime(2020, 7, 31)].index, inplace=False)
            test_data = processed_data.drop(processed_data[processed_data.index <= datetime(2020, 7, 31)].index, inplace=False)

            mySQLManager = MSQLM.MySQLManager("localhost", "root", "toor")
            mySQLManager.connect('stock_market')
            mySQLManager.create('stock', training_data, 'append')
            mySQLManager.connect('stock_market')
            mySQLManager.create('stock_test', test_data, 'append')

def stock_stats(data_frame: pd.DataFrame):
    # TODO: Melhorar as features obtidas adicionando algumas mais úteis.
    stock = StockDataFrame.retype(data_frame)

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

    return stats

def populate_csv(tickers: dict, base_path: str):
    toggle = True

    for ticker in tickers.values():
        raw_data = YAPIH.historical(str(ticker))

        #T oggle para separar a primeira entrada (responsavel por criar o arquivo) das outras.
        if toggle:
            # Cria um dataframe novo juntando uma coluna de tickers + dados originais + features do stockstats
            ticker_serie = pd.Series([str(ticker) for x in range(len(raw_data))], raw_data.index, name="ticker")
            processed_data = pd.concat([ticker_serie, raw_data, stock_stats(raw_data)], axis=1, sort=False)

            # Mini tratamento de dados - Data Cleansing e Preenchimento de campos vazios (aplicado somente ao 'adj close') com a média da coluna
            processed_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            processed_data['adj close'] = processed_data['adj close'].replace(np.nan, value=processed_data['adj close'].mean(), inplace=False)

            # Separação em dados de treino (até a dada marcada no documento de validação) e teste (mas que eu nunca uso como teste não sei pq)
            training_data = processed_data.drop(processed_data[processed_data.index > datetime(2020,7,31)].index, inplace=False)
            test_data = processed_data.drop(processed_data[processed_data.index <= datetime(2020,7,31)].index, inplace=False)

            # Salva os dataframes em CSV (Sobrescreve se o arquivo ja existir)
            training_data.to_csv(base_path+'stock.csv', mode='w', encoding='utf-8', index=True)
            test_data.to_csv(base_path + 'stock_test.csv', mode='w', encoding='utf-8', index=True, header=True)

            toggle = False
        else:
            # Cria um dataframe novo juntando uma coluna de tickers + dados originais + features do stockstats
            ticker_serie = pd.Series([str(ticker) for x in range(len(raw_data))], raw_data.index, name="ticker")
            processed_data = pd.concat([ticker_serie, raw_data, stock_stats(raw_data)], axis=1, sort=False)

            # Mini tratamento de dados - Data Cleansing e Preenchimento de campos vazios (aplicado somente ao 'adj close') com a média da coluna
            processed_data.replace([np.inf, -np.inf], np.nan)
            processed_data['adj close'] = processed_data['adj close'].replace(np.nan, value=processed_data['adj close'].mean(), inplace=False)

            # Separação em dados de treino (até a dada marcada no documento de validação) e teste (mas que eu nunca uso como teste não sei pq)
            training_data = processed_data.drop(processed_data[processed_data.index > datetime(2020, 7, 31)].index, inplace=False)
            test_data = processed_data.drop(processed_data[processed_data.index <= datetime(2020, 7, 31)].index, inplace=False)

            # Salva os dataframes em CSV (Adiciona ao fim do arquivo)
            training_data.to_csv(base_path + 'stock', mode='a', encoding='utf-8', index=True)
            test_data.to_csv(base_path + 'stock_test', mode='a', encoding='utf-8', index=True, header=True)

if __name__ == "__main__":
    run()