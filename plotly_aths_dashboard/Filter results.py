# program to compare an athlete to event results at major

import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Championship_Results.csv") # this is all champs results
df2 = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Athlete Results/Kelsey-Lee Barber.csv") # this is Kels's results
df["RESULT"] = df["RESULT"].astype(float)
df2["Result"] = df2["Result"].astype(float)

event_input = "JT_women" # this will be a user input eventually in Dash
champs_input = "WC_2022"  # will be user input

# this mini function successfully filters csv
# then nlargest for top x results then calculates average from n results
filtresult = df[(df.EVENT == event_input) & (df.CHAMPS == champs_input)]
top3_result = filtresult.nlargest(3, 'RESULT')
top8_result = filtresult.nlargest(8, 'RESULT')
av_oftop3 = top3_result["RESULT"].mean().round(2)
av_oftop8 = top8_result["RESULT"].mean().round(2)
print(av_oftop3, "Top 3 Average - Oregon WC")
print(av_oftop8, "Top 8 Average - Oregon WC")
#print(top3_result)

# New filter for different csv with NASS athlete results
#------------------------------------
filtresult2 = df2[(df2.Season == 2019) & (df2.Name == 'Kelsey-Lee Barber')] # use this for filtering for a specific athlete should be input() in Dash
ath_top5 = filtresult2.nlargest(5, 'Result')
ath_av_oftop5 = ath_top5["Result"].mean().round(2)
print(ath_av_oftop5, "Top 5 Average in given year - NASS athlete ")


# Plot the differences in global results to NASS athlete
#------------------------------------
#fig = px.scatter(df, x='Name', y='PB', hover_data=['Rank'])
#fig.add_hline(y=66.78, annotation_text="Average", annotation_position="bottom right")
#fig.update_traces(marker_size=15) # makes the data point marker larger
#fig.add_trace(go.Scatter(x=['Kelsey-Lee BARBER'], y=[67.70], mode='markers', marker_color='green', marker_size=15, showlegend=False)) #
# the add trace puts a special symbol over the given datapoint
#fig.show()


# when using dash to filter for athlete_select create a list variable for the name
# then put that input() variable in a [list] then using pandas dataframe select only the rows for that athlete
# apply the below example to athlete dash app

#athlete_variable = ['user_input_name_variable']
#filtered_df = dataframe.loc[dataframe['Name'].isin(athlete_variable)]
#print(filtered_df)




