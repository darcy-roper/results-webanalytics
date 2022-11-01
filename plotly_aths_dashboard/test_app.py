# Streamlit dashboard
# to run streamlit package first call - pipenv shell
# followed by - streamlit run *full file path*

import pandas as pd
import streamlit as st
import plotly.express as px

# Heading:
st.title("Web Analytics using Streamlit:")

# Filter the data:
dataframe = pd.read_csv("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/Athlete-results_cleaned data.csv")
dataframe_copy = dataframe.copy()
uniq_names = dataframe_copy['name'].unique()  # filters the athlete names to show options
dataframe_copy["date"] = pd.to_datetime(dataframe_copy["date"], infer_datetime_format=True)  # converts the dates from txt to real dates
group = dataframe_copy[['name', 'discipline']]
ath_events = group.groupby('name')['discipline'].unique().reset_index()
ath_events.set_index('name', inplace=True)
dataframe_copy["discipline"] = dataframe_copy["discipline"].astype(str)


# Add a sidebar:
# adding "select" as the first and default choice
athlete_slt = st.sidebar.selectbox('Select athlete', options=['Select or search an Athlete']+list(ath_events.index))
# display selectbox 2 if manufacturer is not "select"
if athlete_slt != 'Select or search an Athlete':
    for item in ath_events.loc[athlete_slt]:
        event = st.sidebar.selectbox('Select event', options=item)
    st.sidebar.write('You selected ' + athlete_slt + ' ' + event)
#----------------


# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a time period to analyse',
    2012, 2022, (2019, 2021))

# Scatter plot
fig = px.scatter(dataframe_copy[dataframe_copy.values == athlete_slt], x="date", y="mark", title=""+athlete_slt+"- results - true time axis",
             hover_data=['competition', 'country'])
fig.update_yaxes(categoryorder='category ascending')
fig.update_yaxes(tickformat="d")
# Update axes
fig.update_layout(xaxis=dict(autorange=True, rangeslider=dict(autorange=True), type="date"))
st.write(fig)
st.write("Click and drag the ends of the slider to view different date ranges!")

#st.dataframe(dataframe)
