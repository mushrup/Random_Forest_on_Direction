from zipline.api import *
from matplotlib import style
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import csv
style.use('ggplot')

# pythonw -m zipline run -f CompareDailyReturnRate.py --start '+B+' --end '+E+' -o apple.txt

def get_long(df,date,number):
  profit = df.loc[date,'Price'] - df.loc[date,'Price_ytd']
  total_profit = profit*number
  print 'long:',total_profit
  return total_profit

def get_short(df,date,number):
  profit = df.loc[date,'Price_ytd'] - df.loc[date,'Price']
  total_profit = profit*number
  print 'short:',total_profit
  return total_profit

def handle_data(date_df,month_df,date,dummy,Equity):
  profit = 0
  number = 1000
  if dummy == True:
    profit = get_long(month_df,date,number)
  if dummy == False:
    profit = get_short(month_df,date,number)
  Equity = Equity + profit
  date_df.set_value(date,'Equity',Equity)
  return Equity

def keep_data(date_df,date,Equity):
  date_df.set_value(date,'Equity',Equity)

def analyze(df):
  print df
  df.Equity.replace(0, np.nan, inplace=True)
  df.Equity.fillna(method = 'ffill', inplace=True)

  # Graph 1
  plt.figure(figsize=(15,5))
  df['Equity_ytd'] = df.Equity.shift(1)
  df['Equity_change'] = df.Equity/df.Equity[0]
  ax = df.Equity_change.plot(label = 'Algorithms')

  HSI = pd.DataFrame.from_csv('HSI.csv')
  HSI.fillna(method = 'ffill',inplace=True)
  HSI['Close_ytd'] = HSI.Close.shift(1)
  print HSI.Close
  HSI['Close_change'] = HSI['Close']/12105.54981
  HSI.Close_change.plot(ax = ax,label = 'HSI',color='grey')
  plt.legend(loc = 'upper left')

  plt.title('2004 - 2017 Backtest Result')
  plt.savefig('Backtst.png',dpi=500)
  plt.show()

initial = int(sys.argv[1])
df1 = pd.DataFrame.from_csv('Date_template_BT.csv')
df = pd.DataFrame.from_csv('Tencent_adj.csv')
df1['Equity'] = initial
Equity = initial
for index,row in df1.iterrows():
  if index in df.index:
    Equity = handle_data(df1,df,index,df.loc[index]['Dummy'],Equity)
  else:
    keep_data(df1,index,Equity)
    print Equity
analyze(df1)



