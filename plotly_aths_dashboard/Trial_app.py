import pandas as pd
import plotly.express as px

asc_events = ['Javelin Throw', 'High Jump', 'Long Jump', 'Pole Vault', 'Triple Jump', 'Shot Put (5kg)',
              'Discus Throw (1.500kg)', 'Javelin Throw (700g)', 'Decathlon Boys',
              'Shot Put', 'Discus Throw', 'Decathlon', 'Shot Put (6kg)', 'Discus Throw (1.750kg)', 'Decathlon U20',
              'Heptathlon', 'Hammer Throw (6kg)', 'Hammer Throw (5kg)', 'Shot Put (4kg)', 'Hammer Throw',
              'Javelin Throw (500g)', 'Shot Put (3kg)', 'Heptathlon Girls', '35libs Weight', 'Javelin Throw (old)',
              'Hammer Throw (3kg)']
converted_sec_mil = ['400 Metres Hurdles']  # Half Marathon also splits at 1hr mark - needs attention
no_formatting = ['One Hour']
sec_mil = ['400m hurdles (84.0cm)', 'Mixed Shuttle Hurdles Relay', 'Shuttle Hurdles Relay', '4x100 Metres Relay', '100 Yards',
           '100 Metres Hurdles', '150 Metres', '300 Metres', '100m Hurdles (76.2cm)', '60 Metres',
           '60 Metres Hurdles', '110 Metres Hurdles', '100 Metres', '110m Hurdles (91.4cm)', '200 Metres', '400 Metres', '110m Hurdles (99.0cm)']
min_sec_mil = ['8x100 Metres Relay', '500 Metres', 'Cross Country', '4x200 Metres Relay', '2000 Metres', '3000 Metres Steeplechase',
               'Two Miles', 'Mixed 2x2x400m Relay', '12 Kilometres', '4x1500 Metres Relay', '2000 Metres Steeplechase', '300 Metres Hurdles',
               'Distance Medley Relay',  '800 Metres', '3000 Metres', '600 Metres',
               '4x800 Metres Relay', 'One Mile', '5000 Metres Race Walk', '3000 Metres Race Walk', '5000 Metres', '10,000 Metres',
               '10,000 Metres Race Walk', '4x400 Metres Relay', '4x400 Metres Relay Mixed', '1000 Metres', '1500 Metres']
colons_min_sec_mil = ['10 Kilometres Race Walk', 'U20 Race', 'Senior Race']
colons_min_sec = ['5 Kilometres', 'Cross Country 4000m', '5 Kilometres Race Walk']
colons_hr_min_sec = ['15 Kilometers Race Walk', 'Marathon', '15 Kilometres', '20 Kilometres Race Walk', '10 Miles Road',
                     '30 Kilometres Race Walk', '50 Kilometres Race Walk', '35 Kilometres Race Walk']



dataframe = pd.read_csv("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/Athlete-results_cleaned data.csv")
dataframe_copy = dataframe.copy()
uniq_names = dataframe_copy['name'].unique()  # filters the athlete names to show options
group = dataframe_copy[['name', 'discipline']]
ath_events = group.groupby('name')['discipline'].unique().reset_index()
ath_events.set_index('name', inplace=True)

# adding a column to the dataframe with an arbitrary date stored
dataframe_copy["arb_date"] = "06-11-22"
# creating new column with datetime format - combines arbitrary date with the result for datetime formatting
dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['arb_date']) + pd.to_timedelta(dataframe_copy['mark'])
dataframe_copy = dataframe_copy.set_index("datetime")


athlete_slt = "Darcy Roper"
event = "Long Jump"

# determining the dataframe format based on event group lists
if event in asc_events:
    dataframe_copy["mark"] = dataframe_copy["mark"].astype(str)
elif event in sec_mil:  # eg 10.44 for 100m
    dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['datetime'], format="%S.%f")
elif event in min_sec_mil:  # eg 1:45.38 for 800m
    dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['datetime'], format="%M:%S.%f")
elif event in colons_min_sec_mil:  # eg 10:25:63 for 3000m
    dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['datetime'], format="%M:%S:%f")
elif event in colons_min_sec:  # eg 8:31 for 2km
    dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['datetime'], format="%M:%S")
elif event in colons_hr_min_sec:  # eg 2:17:43 for marathon
    dataframe_copy['datetime'] = pd.to_datetime(dataframe_copy['datetime'], format="%H:%M:%S")


##########################################
plot_df = dataframe_copy[(dataframe_copy['name'].str.contains(athlete_slt)) & (dataframe_copy['discipline'].str.contains(event))]
# sort mark
if event in asc_events:
    plot_df.sort_values(by='mark', ascending=True)
    fig = px.scatter(plot_df, x='date', y='mark')
else:
    fig = px.scatter(plot_df, x='date', y='datetime')

# Update axes
# if event in asc_events:
#     fig.axis([min(plot_df['date']), max(plot_df['date']), min(plot_df['mark']), max(plot_df['mark'])])
# elif event in desc_events:
#     fig.axis([min(plot_df['date']), max(plot_df['date']), max(plot_df['mark']), min(plot_df['mark'])])
fig.show()
#############################################

#print(dataframe_copy.dtypes)

# df2 = dataframe_copy[(dataframe_copy['name'].str.contains("Darcy Roper")) & (dataframe_copy['discipline'].str.contains("Long Jump"))]
# df2["mark"] = df2["mark"].astype(float)
# print(df2['mark'])
