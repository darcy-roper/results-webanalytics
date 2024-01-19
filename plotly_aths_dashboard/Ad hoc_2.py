
import pandas as pd

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)


default_athlete_id = 14336705
default_athlete_events = df[df['id'] == default_athlete_id]['discipline'].unique()

# Extract unique disciplines for the default athlete
default_athlete_disciplines = df[df['id'] == default_athlete_id]['discipline'].unique()
# Determine the default event
if 'Javelin Throw' in default_athlete_disciplines:
    default_event = 'Javelin Throw'
elif len(default_athlete_disciplines) > 0:
    # If 'Javelin Throw' is not available but there are other disciplines
    default_event = default_athlete_disciplines[0]
else:
    # If the default athlete has no disciplines listed
    default_event = None

print(default_athlete_id)
print(default_event)
#print(df[df['id'] == default_athlete_id])
