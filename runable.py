import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score

def get_X(token):
	X = pd.read_csv(token+'.csv')
	X.fillna(method = 'ffill',inplace=True)
	X.fillna(method = 'backfill',inplace=True)
	X.dropna(axis = 1,how='all',inplace=True)
	X.drop(['Close'],axis=1,inplace=True)
	X.drop(['OneDayMomentum'],axis=1,inplace=True)
	X1 = X[0:1]
	X2 = X[180:181]
	X3 = X[365:366]
	X4 = X[500:501]
	X5 = X[680:681]
	X6 = X[720:721]
	X7 = X[800:801]
	X8 = X[812:813]
	X9 = X[877:878]
	X10 = X[1180:1181]
	X11 = X[1500:1501]
	X12 = X[1680:1681]
	X13 = X[1320:1321]
	X14 = X[1600:1601]
	X15 = X[1365:1366]
	X16 = X[220:221]
	X17 = X[200:201]
	X18 = X[512:513]
	X19 = X[1000:1001]
	X20 = X[420:421]
	X21 = X[10:11]
	X22 = X[80:81]
	X23 = X[65:66]
	X24 = X[1530:1531]
	X25 = X[1280:1281]
	X26 = X[1420:1421]
	X27 = X[1400:1401]
	X28 = X[1412:1413]
	X29 = X[1477:1478]
	X30 = X[1630:1631]
	X31 = X[5:6]
	X32 = X[185:186]
	X33 = X[370:371]
	X34 = X[505:506]
	X35 = X[685:686]
	X36 = X[725:726]
	X37 = X[805:806]
	X38 = X[817:818]
	X39 = X[882:883]
	X40 = X[1185:1186]
	X41 = X[1505:1506]
	X42 = X[1685:1686]
	X43 = X[1325:1326]
	X44 = X[1605:1606]
	X45 = X[1370:1371]
	X46 = X[225:226]
	X47 = X[205:206]
	X48 = X[517:518]
	X49 = X[1005:1006]
	X50 = X[425:426]
	X51 = X[18:19]
	X52 = X[85:86]
	X53 = X[165:166]
	X54 = X[1525:1526]
	X55 = X[1285:1286]
	X56 = X[1425:1426]
	X57 = X[1405:1406]
	X58 = X[1417:1418]
	X59 = X[1482:1483]
	X60 = X[1635:1636]
	frames = [X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,
	X12,X13,X14,X15,X16,X17,X18,X19,X20,X21,X22,
	X23,X24,X25,X26,X27,X28,X29,X30,X31,X32,X33,
	X34,X35,X36,X37,X38,X39,X40,X41,X42,X43,X44,
	X45,X46,X45,X46,X47,X48,X49,X50,X51,X52,X53,
	X54,X55,X56,X57,X58,X59,X60]
	X = pd.concat(frames)
	return X


ranks = pd.DataFrame([{'Symbol':[],'C_score':[]}])
with open('All_tokens.txt','r') as file:
	for line in file:
		try:
			segments = line.split()
			token = segments[0]
			X = pd.read_csv(token+'.csv')
			y = X.pop('Dummy')
			X.drop(['Prediction','Price'],1,inplace=True)
			numeric_variables = list(X.dtypes[X.dtypes != 'object'].index)
			print numeric_variables
			model = RandomForestRegressor(n_estimators = 300, oob_score = True,random_state = 20)
			model.fit(X[numeric_variables], y)
			y_oob = model.oob_prediction_
			c_score = roc_auc_score(y,y_oob)
			rank = pd.DataFrame([{'Symbol':token,'C_score':c_score}])
			ranks = ranks.append(rank, ignore_index=True)
			X['Predict_RF'] = 0
			idx = 0
			for index,row in X.iterrows():
				if idx > 10:
					df_variable = X.head(idx-1)
					df_variable.drop(['Month','Predict_RF'],1,inplace=True)
					print model.predict(df_variable).mean()
					X.set_value(index,'Predict_RF',model.predict(df_variable).mean())
				idx += 1
			print X
			X.to_csv('Tencent_RF.csv')
		except Exception as e:
			print (e,token)
	ranks = ranks[1:]
	ranks.sort('C_score',inplace=True)
	ranks.to_csv('C_score_ranking.csv',encoding='utf-8')


