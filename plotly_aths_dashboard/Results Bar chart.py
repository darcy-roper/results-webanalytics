# This is a trail program to run plotly visualisations through code
# Kelsey Lee-Barber's performances are used, as taken from WA website

import pandas as pd
import plotly.express as px

#athlete_name = input("Get results for athlete: ")

# reads the csv file in folder location specified
df = pd.read_csv('somethingNew.csv', sep='|')

# converts int to a str so the data becomes discrete not continuous
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# defines the elements in the bar graph and actions when hovering
fig = px.scatter(df[df['id']==14550669], x="date", y="resultscore", title="Darcy Roper - rolling 5 comp trend line - true time axis")

# appends the y-axis to smaller range
fig.update_yaxes(range=[min(df["resultscore"]-.10), max(df["resultscore"]+.10)])
fig.update_yaxes(rangemode='normal')
#fig.update_traces(mode='markers', marker_size=10)

# displays the graph
fig.show()


# program successfully reads document and displays graph in browser
