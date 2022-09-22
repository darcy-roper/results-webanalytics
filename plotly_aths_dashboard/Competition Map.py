# program to display competitions in map of world

import pandas as pd
import plotly.express as px
df = pd.read_csv("Datasets/Athlete Results/Darcy Roper.csv")
fig = px.scatter_geo(df, locations="Ctry", color="Continent", projection="natural earth", size="Competition_Count")

fig.show()
