from zipline.api import *
from matplotlib import style
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
style.use('ggplot')

# pythonw -m zipline run -f CompareDailyReturnRate.py --start '+B+' --end '+E+' -o apple.txt

def get_LongPricing(portfolio,date):
  total = 0
  for token in portfolio:
    try:
      df = pd.DataFrame.from_csv(token+'_adj_.csv')
      price = df.loc[date,'Close']
      total = price + total
    except:
      pass
  return total

def get_ShortPricing(portfolio,date):
  total = 0
  for token in portfolio:
    try:
      df = pd.DataFrame.from_csv(token+'_adj_.csv')
      price = df.loc[date,'Close']
      total = price + total
    except:
      pass
  return total

def handle_data(df,date,longs,shorts):
    Long_price = get_LongPricing(longs,date)
    Short_price = get_ShortPricing(shorts,date)
    Equity = Long_price - Short_price
    try:
      Leverage = Short_price/Equity
    except:
      Leverage = 0
    print date,Long_price,-Short_price,Equity,Leverage
    df.set_value(date,'Long',Long_price)
    df.set_value(date,'Short',-Short_price)
    df.set_value(date,'Equity',Equity)
    df.set_value(date,'Leverage',Leverage)

def analyze(df):
  df.Long.replace(0, np.nan, inplace=True)
  df.Short.replace(0, np.nan, inplace=True)
  df.Equity.replace(0, np.nan, inplace=True)
  df.Leverage.replace(0, np.nan, inplace=True)

  df.Long.fillna(method = 'ffill', inplace=True)
  df.Short.fillna(method = 'ffill', inplace=True)
  df.Equity.fillna(method = 'ffill', inplace=True)
  df.Leverage.fillna(method = 'ffill', inplace=True)

  # Graph 1
  plt.figure(figsize=(50,5))
  df['Long_ytd'] = df.Long.shift(1)
  df['Long_change'] = df.Long/df.Long[0]

  df['Equity_ytd'] = df.Equity.shift(1)
  df['Equity_change'] = df.Equity/df.Equity[0]

  ax = df.Long_change.plot()
  ax.set_title('Long Short Position')
  df.Equity_change.plot(ax = ax)

  # Graph 1
  plt.figure(figsize=(50,5))
  HSI = pd.DataFrame(pd.read_csv('HSI.csv',encoding = 'utf-8'))
  HSI.fillna(method = 'ffill',inplace=True)
  HSI['Close_ytd'] = HSI.Close.shift(1)
  HSI['Close_change'] = HSI.Close/HSI.Close[0]
  HSI.Close_change.plot(ax = ax)

  # Graph 2
  plt.figure(figsize=(50,5))
  ax2 = df.Leverage.plot()
  ax2.set_title('Leverage rate')
  plt.show()

df = pd.DataFrame(pd.read_csv('bridge.csv',encoding = 'utf-8',converters={'long': lambda x: str(x),'short': lambda x: str(x)}))
longs = df['long']
shorts = df['short']
df = pd.DataFrame(pd.io.parsers.read_csv('Date_template_BT.csv',skipinitialspace=True))
df.set_index('Date', inplace=True)
for index,row in df.iterrows():
  handle_data(df,index,longs,shorts)
analyze(df)



