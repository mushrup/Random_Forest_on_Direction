import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys
matplotlib.style.use('ggplot')

def see_relation(df,param):
	# Graph 1
	plt.figure(figsize=(50,5))
	ax = df[param].plot(figsize=(50,5),kind = 'hist',bins=40)
	ax.set_title(param+' Histogram')

	# Graph 2
	plt.figure(figsize=(50,5))
	plt.scatter(df[param], df['Close_grow'], alpha=0.9)
	plt.title('Annual Price Change(Y) and '+param+'(X)')

	# Graph 3
	plt.figure(figsize=(50,5))
	ax3 = df['Close_grow'].plot(figsize=(50,5),kind = 'hist',bins=40)
	ax3.set_title('Annual Price Change Histogram')

	# Graph 4
	plt.figure(figsize=(50,5))
	df1 = df.tail(162)
	ax3 = df1['Close_grow'].plot(figsize=(50,5),kind = 'hist',bins=40)
	ax3.set_title('BackTest')

	plt.show()

# input
param = 'C_score'

df = pd.read_csv('C_score_ranking_adj.csv',converters={'Symbol': lambda x: str(x)})
see_relation(df,param)