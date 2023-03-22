# read csv dataframe to pandas

import pandas as pd

df = pd.read_csv('somethingNew.csv', sep='|')

dff = df[df['id']==14550669]
dff['Count'] = dff.groupby(['country'])['__typename'].transform('count')

print(dff)
