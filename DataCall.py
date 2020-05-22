from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
import numpy as np
#from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import mplfinance as mpf

def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 5  #variable

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 

if ret1 == RET_OK:
    print(data1)
    print(data1['code'][0])    # 取第一条的股票代码
    print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)
    
'''#store data to CSV file
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv

print('----------------------------')
'''

quote_ctx.close() #close connection 


#print(len(data1.index))
LastData = data1.time_key[len(data1.index) - 1] #find the last index

#Backtest
# Initialize the `signals` DataFrame with the `signal` column, index is the time
signals = pd.DataFrame(index=data1.time_key)
plotdata1 = pd.DataFrame(index=data1.time_key)
print(plotdata1.dtypes)
data1['time_key'] = pd.to_datetime(data1['time_key'],)
plotdata1['time_key'] =  pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
print('--------data types------')
print(data1.dtypes)
pd.to_datetime(plotdata1)
signals['signal'] = 0.0


#RSI
signals['RSI'] = abstract.RSI(data1.close,6)
SMA10 = abstract.SMA(data1.close,timeperiod=10)

#RVI
Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))
      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))
signals['RVI'] = RVI = (Nem/6)/(Dem/6)
signals['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
print('------------------rvi---------------------')

# Create signals

#create temporary data for condition check
temp1 = signals['RSI'][:-1]
temp1 = temp1.shift(1)
temp2 = signals['RSI'][:-2]
temp2 = temp1.shift(2)
signals['signal'] = np.where((signals['RSI'] <= 20) | (temp1 <=20) | (temp2 <=20) , 1.0, 0.0)

signals['positions'] = signals['signal'].diff()
print('-----------------signal-----------------')

print(signals)

print('-------------------data----------')
#data1.index = data1['time_key']
#data1.set_index('time_key', inplace=True)
#data1.index.name = 'Date'
#data1 = data1.set_index('time_key')
#data1.rename(columns={'open':'Open', 'close':'Close','high':'High','low':'Low'}, inplace=True) #rename columns
print(data1)

#sma_10 = talib.SMA(np.array(data1['Close']), 10)
#sma_30 = talib.SMA(np.array(data1['Close']), 30)




#創建圖框
fig = plt.figure(figsize=(24, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xticks(range(0, len(data1.index), 10))
ax.set_xticklabels(data1.index[::10],rotation=90)

ax2 = fig.add_axes([0,0.1,1,0.2])
ax2.set_xticks(range(0, len(data1.index), 10))
ax2.set_xticklabels(data1.index[::10],rotation=90)

ax3 = fig.add_axes([0,0,1,0.1])
#設定座標數量及所呈現文字

#使用mpl_finance套件candlestick2_ochl
'''
mpf.candlestick2_ochl(ax, data1['open_price'], data1['close_price'], data1['high'],
                      data1['low'], width=0.6, colorup='r', colordown='g', alpha=0.75); 
'''
#mpf.plot(data1)
#mpf.volume_overlay(ax2, data1['open_price'], data1['close_price'], data1['volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
#plt.show()
'''
reformatted_data = dict()
reformatted_data['Date'] = []
reformatted_data['Open'] = []
reformatted_data['High'] = []
reformatted_data['Low'] = []
reformatted_data['Close'] = []
reformatted_data['Volume'] = []
for dict in data1:
    reformatted_data['Date'].append(datetime.fromtimestamp(dict['time_key']))
    reformatted_data['Open'].append(dict['open'])
    reformatted_data['High'].append(dict['high'])
    reformatted_data['Low'].append(dict['low'])
    reformatted_data['Close'].append(dict['close'])
    reformatted_data['Volume'].append(dict['volume'])
print("reformatted data:", reformatted_data)
pdata = pd.DataFrame.from_dict(reformatted_data) 
pdata.set_index('Date', inplace=True)
mpf.plot(pdata)
'''


plotdata1['open'] = data1.open
plotdata1['high'] = data1.high
plotdata1['low'] = data1.low
plotdata1['close'] = data1.close
plotdata1['volume'] = data1.volume


mpf.plot(plotdata1)
print(data1.dtypes)
