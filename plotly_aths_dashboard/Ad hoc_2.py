
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time

# Load data
df = pd.read_csv('Athlete_Cleansed2023.csv', sep='|')
#df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# #fishing for season's bests
# filtered_data = df[df['id'] == 14455361]
# dfb = filtered_data.copy()
# dfb['season'] = dfb['date'].dt.strftime('%Y')
# dfb['season'] = dfb['season'].astype(int)
# dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')

# Get unique values in the 'discipline' column
unique_disciplines = df['discipline'].unique()

# Print unique disciplines
print(unique_disciplines)
