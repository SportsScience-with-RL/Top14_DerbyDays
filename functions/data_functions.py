import pandas as pd
import numpy as np
from scipy import stats
import time

def load_data(match):
    teams = match.split(' - ')
    data = pd.read_csv(f'data/Match_{teams[0]}_{teams[1]}.csv', encoding='latin1')

    data['Durée'] = [((time.localtime(t).tm_min*60) + time.localtime(t).tm_sec) for t in[e-s for s, e in zip(data['Start_time'], data['End_time'])]]

    data['Ratio Rucks/Passes'] = round(data['Ruck'] / data['Passe'], 2)
    data['Ratio Rucks/Passes'] = data['Ratio Rucks/Passes'].fillna(0)
    data.loc[data['Passe']==0, 'Ratio Rucks/Passes'] = 0

    data['Progression Zones'] = data['End_zone_value'] - data['Start_zone_value']

    data['Jeu debout'] = data['Passe'] + data['Offload']

    data['PZtimeline'] = [(-d) if p==m.split(' - ')[1] else d for d, p, m in zip(data['Durée'], data['Possession'], data['Match'])]

    data['Jeu debout'] = data['Passe'] + data['Offload']
    data['Utilisation Jeu au pied'] = data['Dégagement'] + data['Jeu au pied']

    return data


def descriptive_tbl(data, metric, period=False):
    if period:
        gb_ = ['Possession', 'Chrono']
        as_idx = True
    else:
        gb_ = ['Possession']
        as_idx = False

    agg_func = {
        metric: ['count', lambda x: f"{int(stats.variation(x)*100)}%" if np.mean(x) > 0 else '0%', 'mean', 'min',
            lambda x: x.quantile(.25), 'median', lambda x: x.quantile(.75), 'max']
            }
    
    tbl = data.groupby(gb_, as_index=as_idx).agg(agg_func).round(0)
    tbl = tbl.rename(columns={'count':'Nb', '<lambda_0>': 'Coef. Var.', 'mean': 'Moy.',
                              'min': 'Min.', '<lambda_1>': 'Q1', 'median': 'Méd.', 
                              '<lambda_2>': 'Q3', 'max': 'Max.'})
    tbl.columns = tbl.columns.droplevel()
    
    return tbl