# This is a trail program to run plotly visualisations through code
# Kelsey Lee-Barber's performances are used, as taken from WA website

import pandas as pd
import plotly.express as px

#athlete_name = input("Get results for athlete: ")

# reads the csv file in folder location specified
dfb = pd.read_csv("Datasets/Athlete Results/" + "Darcy Roper" + ".csv")

# converts int to a str so the data becomes discrete not continuous
dfb["Season"] = dfb["Season"].astype(str)

dfb["Date"] = pd.to_datetime(dfb["Date"], infer_datetime_format=True)

# defines the elements in the bar graph and actions when hovering
fig = px.scatter(dfb, x="Date", y="Result", title="Darcy Roper - rolling 5 comp trend line - true time axis",
             hover_data=['Competition', 'Country'], trendline='rolling', trendline_options=dict(window=5))

# appends the y-axis to smaller range
fig.update_yaxes(range=[min(dfb["Result"]-.10), max(dfb["Result"]+.10)])
fig.update_yaxes(rangemode='normal')
#fig.update_traces(mode='markers', marker_size=10)

# displays the graph
fig.show()


# program successfully reads document and displays graph in browser
