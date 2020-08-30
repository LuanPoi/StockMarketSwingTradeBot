import pandas as pd
from stockstats import StockDataFrame

dataFrame = pd.read_csv('/home/andromeda/programacao/TCC/StockMarketSwingTradeBot/Resources/Datasets/stock_market_stock.csv')
stock = StockDataFrame.retype(dataFrame)


# volume delta against previous day
print(stock.get('volume_delta'))

# open delta against next 2 day
print(stock.get('open_2_d'))

# open price change (in percent)) between today and the day before yesterday
# 'r' stands for rate.
print(stock.get('open_-2_r'))

# CR indicator, including 5, 10, 20 days moving average
print(stock.get('cr'))
print(stock.get('cr-ma1'))
print(stock.get('cr-ma2'))
print(stock.get('cr-ma3'))

# volume max of three days ago, yesterday and two days later
aux = stock.get('volume_-3,2,-1_max')

# volume min between 3 days ago and tomorrow
print(stock.get('volume_-3~1_min'))

# KDJ, default to 9 days
print(stock.get('kdjk'))
print(stock.get('kdjd'))
print(stock.get('kdjj'))

# three days KDJK cross up 3 days KDJD
print(stock.get('kdj_3_xu_kdjd_3'))

# 2 days simple moving average on open price
print(stock.get('open_2_sma'))

# MACD
print(stock.get('macd'))
# MACD signal line
print(stock.get('macds'))
# MACD histogram
print(stock.get('macdh'))

# bolling, including upper band and lower band
print(stock.get('boll'))
print(stock.get('boll_ub'))
print(stock.get('boll_lb'))

# close price less than 10.0 in 5 days count
print(stock.get('close_10.0_le_5_c'))

# CR MA2 cross up CR MA1 in 20 days count
print(stock.get('cr-ma2_xu_cr-ma1_20_c'))

# count forward(future)) where close price is larger than 10
print(stock.get('close_10.0_ge_5_fc'))

# 6 days RSI
print(stock.get('rsi_6'))
# 12 days RSI
print(stock.get('rsi_12'))

# 10 days WR
print(stock.get('wr_10'))
# 6 days WR
print(stock.get('wr_6'))

# CCI, default to 14 days
print(stock.get('cci'))
# 20 days CCI
print(stock.get('cci_20'))

# TR (true range))
print(stock.get('tr'))
# ATR (Average True Range))
print(stock.get('atr'))

# DMA, difference of 10 and 50 moving average
print(stock.get('dma'))

# DMI
# +DI, default to 14 days
print(stock.get('pdi'))
# -DI, default to 14 days
print(stock.get('mdi'))
# DX, default to 14 days of +DI and -DI
print(stock.get('dx'))
# ADX, 6 days SMA of DX, same as print(stock.get('dx_6_ema'))
print(stock.get('adx'))
# ADXR, 6 days SMA of ADX, same as print(stock.get('adx_6_ema'))
print(stock.get('adxr'))

# TRIX, default to 12 days
print(stock.get('trix'))
    # TRIX based on the close price for a window of 3
print(stock.get('close_3_trix'))
# MATRIX is the simple moving average of TRIX
print(stock.get('trix_9_sma'))
# TEMA, another implementation for triple ema
print(stock.get('tema'))
    # TEMA based on the close price for a window of 2
print(stock.get('close_2_tema'))

# VR, default to 26 days
print(stock.get('vr'))
# MAVR is the simple moving average of VR
print(stock.get('vr_6_sma'))
