import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def collect_calibrations(directory=None):
	"""
	leave directory as None for current working directory

	returns a dataframe of daily calibration details
	"""
	if directory == None:
		files = [f for f in os.listdir() if f.endswith('.csv')]
	else:
		files = [f for f in os.listdir(directory) if f.endswith('.csv')]
	
	dfs = []
	for f in files:
		dfs.append(pd.read_csv(f).iloc[:,1:])

	dfs = [df for df in dfs if not df.empty and not df.isna().all().all()]
	df = pd.concat(dfs, ignore_index=True).dropna()

	df = df[df['relative_error']<1]
	difference = df['heston']-df['black_scholes']
	relative_error = df['heston']/df['black_scholes']-1
	difference, relative_error = difference.dropna(),relative_error.dropna()
	
	MRE = np.mean(relative_error)
	MARE = np.mean(np.abs(relative_error))
	MAE = np.mean(np.abs(difference))
	RMSE = np.sqrt(np.mean(difference**2))

	print(f"MRE: {round(MRE*100,4)}%",f"\nMARE: {round(MARE*100,4)}%",f"\nMAE: {MAE}",f"\nRMSE: {RMSE}")

	bins = int(np.sqrt(df.shape[0]))
	line = np.arange(1,df.shape[0]+1,1)
	plt.figure()
	plt.scatter(line,np.sort(df['heston']),color='purple',s=1,label='Heston')
	plt.scatter(line,np.sort(df['black_scholes']),color='green',s=1,label='Black Scholes')
	# plt.plot(np.linspace(0,df.shape[0],2),np.linspace(0,max(max(df['heston']),max(df['black_scholes'])),2),color='black',label='normal?')
	plt.title('QQ-Plot of Heston vs Black Scholes prices')
	plt.ylabel('price')
	plt.xlabel('ordinal position')
	plt.legend()
	plt.show()

	calibrations = df[
		[
			'spot_price', 'theta',
			'kappa', 'eta', 'rho', 'v0', 'calculation_date', 'risk_free_rate',
			'dividend_rate'
		]
	].drop_duplicates().reset_index(drop=True).copy()

	calibrations['calculation_date'] = pd.to_datetime(calibrations['calculation_date'])
	calibrations = calibrations.sort_values(by='calculation_date')
	print(calibrations)
	plotcols = ['calculation_date','spot_price','theta','kappa','rho','eta','v0']
	plotvalues = calibrations[plotcols].copy().set_index(['calculation_date'])
	for col in plotvalues.columns:
		plt.figure()
		plt.plot(plotvalues[col])
		plt.title(col.replace('_',' '))
		plt.show()
	return calibrations
