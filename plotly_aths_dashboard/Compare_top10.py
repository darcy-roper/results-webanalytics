# successfully runs scatter plot using csv file and plots on two y-axes

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Event_Rankings_Top10.csv")
df2 = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Athlete Results/Kelsey-Lee Barber.csv") # this is Kels's results but will change to all athletes csv
df["PB"] = df["PB"].astype(float)
df["SB"] = df["SB"].astype(float)

event_input = "JT_women" # this will be a user input eventually in Dash

year_input = 2022  # this will be a user input eventually in Dash but needed for SB filtering
slct_athlete = "Kelsey-Lee Barber"

# makes a copy of the data frame for filtering
dff = df.copy()
dff = dff[(dff.EVENT == event_input)]

# makes a copy of the data frame 2 for filtering
dff2 = df2.copy()
dff2 = dff2[(dff2.Name == slct_athlete) & (dff2.Season == year_input)]

# Create figure
fig = go.Figure()

# The entries for the NASS athlete
# ---------------------------------------------------------
# Add trace for athlete PB to highlight
filt_PB = dff2["PB"].max()
fig.add_trace(go.Scatter(x=[slct_athlete], y=[filt_PB], mode='markers', marker_symbol='star-diamond-dot', marker_color='purple', marker_size=15,
                         showlegend=False, hovertemplate="%{x} %{y} <extra>PB</extra>")) # the 'extra' tags change the "trace" label on the marker
# Add trace for athlete SB to highlight
filt_SB = dff2["SB"].max()
fig.add_trace(go.Scatter(x=[slct_athlete], y=[filt_SB], mode='markers', marker_symbol='star-diamond-dot', marker_color='orange', marker_size=13,
                         showlegend=False, hovertemplate="%{x} %{y} <extra>SB</extra>"))


# The entries from the CSV data as taken from World athletics
# ---------------------------------------------------------
fig.add_trace(go.Scatter(x=dff['Name'], y=dff['PB'], name="PB", mode='markers', marker_size=18, marker_color="green",
                         text=dff['Rank'], hovertemplate="%{x} %{y} <br> Current World Rank = %{text}"))
fig.add_trace(go.Scatter(x=dff['Name'], y=dff['SB'], name="SB", mode='markers', marker_size=15, marker_color="blue",
                         text=dff['Rank'], hovertemplate="%{x} %{y} <br> Current World Rank = %{text}"))


# Update the horizontal lines for average figures
# ---------------------------------------------------------
# Add horizontal line for averages
av_PBs = dff["PB"].mean().round(2)
av_SBs = dff["SB"].mean().round(2)
fig.add_hline(y=av_PBs, annotation_text="Average PB", annotation_position="bottom right", line_color="green")
fig.add_hline(y=av_SBs, annotation_text="Average SB", annotation_position="bottom right", line_color="blue")


# Add figure title
fig.update_layout(
    title_text="World Top 10 (points) PBs/SBs - Compared to Athlete")

# Set x-axis titles
fig.update_xaxes(title_text="Athlete Name")
fig.update_yaxes(title_text="Result (m)")

fig.show()
