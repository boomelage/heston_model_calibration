import numpy as np
import pandas as pd
from itertools import product
from quantlib_pricers import vanilla_pricer
from model_settings import ms
vanp = vanilla_pricer()


def test_calibration(s,K,T,
	r,heston_parameter_pdSeries
	):

	contracts = pd.DataFrame(product([s],K,T),columns=['spot_price','strike_price','days_to_maturity'])
	n = contracts.shape[0]
	contracts['risk_free_rate'] = np.tile(r,n)
	contracts['dividend_rate'] = np.tile(0.0,n)
	contracts[heston_parameters.index] = np.tile(heston_parameters.values,(n,1))
	contracts['black_scholes'] = vanp.df_numpy_black_scholes(contracts)
	contracts['heston'] = vanp.df_heston_price(contracts)


import os
from pathlib import Path
root = Path(__file__).parent.parent.parent.parent.resolve().absolute()


path = os.path.join(root,'OneDrive - rsbrc','git_data','cboe_intraday_generation_prototype','calibrations')
files = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.csv')][0]

pnames = ['kappa','theta','rho','eta','v0']
print(files)
df = pd.read_csv(files).iloc[0]
heston_parameters = df[pnames].squeeze()

print(heston_parameters)
print(type(heston_parameters))

test_calibration(100,[90,100,110],[90],0.04,heston_parameters)
