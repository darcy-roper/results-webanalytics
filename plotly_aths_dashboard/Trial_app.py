import pandas as pd
import numpy as np

dataframe = pd.read_csv("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/Athlete-results_cleaned data.csv")
dataframe_copy = dataframe.copy()
uniq_names = dataframe_copy['name'].unique()  # filters the athlete names to show options
group = dataframe_copy[['name', 'discipline']]
ath_events = group.groupby('name')['discipline'].unique().reset_index()
ath_events.set_index('name', inplace=True)

# for item in ath_events.loc['Darcy Roper']:
#     print(item)
#print(ath_events.loc['Darcy Roper'])

all_ev = dataframe_copy['discipline'].unique()
print(all_ev)
