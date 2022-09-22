# program to display competitions in map of world

import pandas as pd
import plotly.express as px
df = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/NASS list (20-21).csv")
fig = px.scatter_geo(df, locations="Ctry", color="Continent", projection="natural earth", size="Competition_Count")

fig.show()
