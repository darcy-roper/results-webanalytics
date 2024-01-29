
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# Ignoring all records where 'notlegal' = True
filtered_data_athlete = df[(df['id'] == 14550669) &
                           (df['discipline'] == "Long Jump") &
                           (df['notlegal'] != "True")] # only legal performances

top_10 = filtered_data_athlete.nlargest(10, 'resultscore') # gets 10 best legal performances

print(top_10['mark'])
