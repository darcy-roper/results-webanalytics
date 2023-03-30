# read csv dataframe to pandas

import pandas as pd
import plotly.express as px

df = pd.read_csv('somethingNew.csv', sep='|')

dff = df[df['id']==14550669]
#dff['Count'] = dff.groupby(['country'])['__typename'].transform('count')

# convert date in dff to dattimeseries
#dff['date'] = pd.to_datetime(df['date'])
#season_best = dff.set_index(['date']).groupby(pd.Grouper(freq='A'))['resultscore'].nlargest(3)

#dff['season'] = dff['season'].astype(int)
# add column for season placing count
#dff['num_place'] = dff.groupby(['category', 'place'])['place'].transform('count')
#abc = dff[['category', 'place']].value_counts()
abc = dff.groupby(['place', 'category']).size().reset_index(name='counts')
abc1 = dff.groupby(['place', 'category']).size().reset_index(name='number_of_placings')


print(abc1)
#print(abc)

# plotly colors
# fig = px.colors.sequential.swatches_continuous()
# fig.show()
