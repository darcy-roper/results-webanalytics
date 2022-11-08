# Streamlit dashboard
# to run streamlit package first call - pipenv shell
# followed by - streamlit run *full file path*

import pandas as pd
import streamlit as st
import plotly.express as px


asc_events = ['Javelin Throw', 'High Jump', 'Long Jump', 'Pole Vault', 'Triple Jump', 'Shot Put (5kg)',
              'Discus Throw (1.500kg)', 'Javelin Throw (700g)', 'Decathlon Boys', '110m Hurdles (99.0cm)',
              'Shot Put', 'Discus Throw', 'Decathlon', 'Shot Put (6kg)', 'Discus Throw (1.750kg)', 'Decathlon U20',
              'Heptathlon', 'Hammer Throw (6kg)', 'Hammer Throw (5kg)', 'Shot Put (4kg)', 'Hammer Throw',
              'Javelin Throw (500g)', 'Shot Put (3kg)', 'Heptathlon Girls', '35libs Weight', 'Javelin Throw (old)',
              'Hammer Throw (3kg)']
desc_events = ['8x100 Metres Relay', 'One Hour', '500 Metres', '10 Miles Road', 'Cross Country',
               '400m hurdles (84.0cm)', 'Cross Country 4000m', '4x200 Metres Relay', 'Mixed Shuttle Hurdles Relay',
               'Shuttle Hurdles Relay', '2000 Metres', '15 Kilometers Race Walk', 'U20 Race', '3000 Metres Steeplechase',
               'Senior Race', 'Marathon', 'Two Miles', 'Mixed 2x2x400m Relay', '4x100 Metres Relay', '100 Yards',
               '100 Metres Hurdles', '150 Metres', '300 Metres', '15 Kilometres', '12 Kilometres', '4x1500 Metres Relay',
               '2000 Metres Steeplechase', '300 Metres Hurdles', '400 Metres Hurdles', '100m Hurdles (76.2cm)',
               'Distance Medley Relay', '5 Kilometres', '800 Metres', '3000 Metres', '600 Metres', '4x800 Metres Relay',
               'One Mile', '5000 Metres Race Walk', '20 Kilometres Race Walk', '10 Kilometres Race Walk',
               '3000 Metres Race Walk', '5000 Metres', '10,000 Metres', 'Half Marathon', '10,000 Metres Race Walk',
               '10 Kilometres', '30 Kilometres Race Walk', '50 Kilometres Race Walk', '5 Kilometres Race Walk',
               '35 Kilometres Race Walk', '4x400 Metres Relay', '4x400 Metres Relay Mixed', '60 Metres', '1000 Metres',
               '60 Metres Hurdles', '110 Metres Hurdles', '100 Metres', '110m Hurdles (91.4cm)', '200 Metres', '400 Metres', '1500 Metres'
               ]

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
#dataframe_copy["mark"] = dataframe_copy["mark"].astype(str)



# Add a sidebar:
# adding "select" as the first and default choice
athlete_slt = st.sidebar.selectbox('Select athlete', options=['Select or search an Athlete']+list(ath_events.index))
# display selectbox 2 if manufacturer is not "select"
if athlete_slt != 'Select or search an Athlete':
    for item in ath_events.loc[athlete_slt]:
        event = st.sidebar.selectbox('Select event', options=item)
    st.sidebar.write('You selected ' + athlete_slt + ' ' + event)


# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a time period to analyse',
    2012, 2022, (2019, 2021))

# Scatter plot
plot_df = dataframe_copy[(dataframe_copy['name'].str.contains(athlete_slt)) & (dataframe_copy['discipline'].str.contains(event))]
if event in asc_events:
    plot_df["mark"] = plot_df["mark"].astype(float)
elif event in desc_events:
    plot_df["mark"] = plot_df["mark"].astype(str)
fig = px.scatter(plot_df
                 , x="date", y="mark", color='discipline', symbol='discipline', title=""+athlete_slt+"- results - true time axis",
                 hover_data=['competition', 'country'])

# Update axes
fig.update_layout(xaxis=dict(autorange=True, rangeslider=dict(autorange=True), type="date"))
if event in asc_events:
    fig.update_yaxes(categoryorder='min ascending')
elif event in desc_events:
    #fig.update_layout(categoryorder='min descending')
    fig.update_layout(autotypenumbers='convert types')
st.write(fig)
st.write("Click and drag the ends of the slider to view different date ranges!")

