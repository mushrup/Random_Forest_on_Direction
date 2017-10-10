import sys
import os
import pandas as pd

def add_change(token_df,df,index,term):
	total_change = token_df[term][1642]/token_df[term][0]
	annual_change = total_change**0.225 - 1 
	df.loc[index,term+'_grow'] = annual_change 

# input
param = ['Research_and_development']
#term = sys.argv
#param.append(term[1])

df = pd.read_csv('C_score_ranking.csv',converters={'Symbol': lambda x: str(x)})
for index,row in df.iterrows():
	token = row['Symbol']
	token_df = pd.read_csv(token+'_lagged_90d.csv',converters={'Symbol': lambda x: str(x)})
	token_df.fillna(method = 'bfill',inplace = True)
	# Column 1
	add_change(token_df,df,index,'Close')

	# Column 2
	try:
		add_change(token_df,df,index,'Revenue')
	except:
		pass

	# Column 3 , where input is!!!
	for term in param:
		try:
			add_change(token_df,df,index,term)
		except:
			pass
df.to_csv('C_score_ranking_adj.csv',encodng='utf-8')
os.system('python draw_hist.py '+term)