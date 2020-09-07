import  Scripts.DataManager.Trainer as Trainer
import  Scripts.DataManager.MySQLManager as MSQLM
import Scripts.DataManager.YahooAPIHandler as YAPIH

from datetime import datetime
import pandas as pd
from stockstats import StockDataFrame

tickers = {
        "Inter": "BIDI4.SA",
        "Petrobras": "PETR4.SA",
        "Vale": "VALE3.SA",
        "Itau": "ITUB4.SA",
        "Ambev": "ABEV3.SA",
        "Sinqia": "SQIA3.SA",
        "iShares_Bovespa": "BOVA11.SA"
}


def run():
    current_ticker = tickers['Itau']

    # data_set = load_data(current_ticker)
    # true_values = load_true_values(current_ticker)

    # TODO: Remover o populate após implementar a requisição pelo banco e colocar a requisição aqui
    raw_data = YAPIH.historical(ticker=tickers['Itau'])
    training_data = populate_mysql(raw_data)
    test_data = raw_data.drop(raw_data[raw_data.index < datetime(2020, 7, 31)].index, inplace=False)
    Trainer.run(training_data, test_data.head(120))


def load_data(ticker):
    mySQLManager = MySQLManager("localhost", "root", "toor")

    mySQLManager.connect("stock_market")
    return mySQLManager.read(table_name="stock", select_items=["ticker", "date", "adj_close"], ticker=ticker, where_condition="date < \'2019-07-12\'",
                                verbose=False)

def load_true_values(ticker):
    mySQLManager = None
    mySQLManager = MySQLManager("localhost", "root", "toor")
    mySQLManager.connect("stock_market")
    true_values = mySQLManager.read(table_name="stock", select_items=["ticker", "date", "adj_close"], ticker=ticker,
                                    where_condition="date >= \'2019-07-12\' limit 120", verbose=False)
    return true_values

def populate_mysql(raw_data):
    # Pega os dados da api e remove aqueles alem do limite de data
    raw_data.drop(raw_data[raw_data.index > datetime(2020,7,31)].index, inplace=True)
    #calcula e adiciona os dados do stats_model no dataframe
    processed_data = pd.concat([stock_stats(raw_data), raw_data], axis=1, sort=False)
    # Todo: Fazer a inserção dos dados no MySQL
    return processed_data

def stock_stats(data_frame: pd.DataFrame):
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

if __name__ == "__main__":
    run()