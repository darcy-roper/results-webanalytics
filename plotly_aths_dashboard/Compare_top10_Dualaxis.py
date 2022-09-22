#successfully runs scatter plot using csv file and plots on two y-axes

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("Datasets/Event_Rankings_Top10.csv")
df["PB"] = df["PB"].astype(float)
df["SB"] = df["SB"].astype(float)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df['Name'], y=df['PB'], name="yaxis data"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['Name'], y=df['SB'], name="yaxis data"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Double Y Axis Example"
)

# Set x-axis title
fig.update_xaxes(title_text="xaxis title")

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

fig.show()
