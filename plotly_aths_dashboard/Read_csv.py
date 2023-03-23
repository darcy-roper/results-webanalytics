# read csv dataframe to pandas

import pandas as pd

df = pd.read_csv('somethingNew.csv', sep='|')

dff = df[df['id']==14550669]
#dff['Count'] = dff.groupby(['country'])['__typename'].transform('count')

# convert date in dff to dattimeseries
dff['date'] = pd.to_datetime(df['date'])
#season_best = dff.set_index(['date']).groupby(pd.Grouper(freq='A'))['resultscore'].nlargest(3)

# add column for season
dff['season'] = dff['date'].dt.strftime('%Y')
dff['season'] = dff['season'].astype(int)
# add column for season best result
dff['sn_best'] = dff.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')

print(dff)

print(dff.dtypes)
