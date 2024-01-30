
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

filtered_data = df[df['id'] == 14455361]
dfb = filtered_data.copy()
dfb['season'] = dfb['date'].dt.strftime('%Y')
dfb['season'] = dfb['season'].astype(int)
dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')

print(dfb)
