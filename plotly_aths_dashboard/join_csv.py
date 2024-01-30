# File to join by athlete id using pandas
# This program also performs statistical analysis on the data frame

import pandas as pd
import statsmodels.api as sm

#read csvs
noname_df = pd.read_csv('Athlete_Cleansed2023.csv', sep='|')
name_ids = pd.read_csv('Datasets/NASS list (23-24).csv', sep=',')
# the nass list csv was extracted from the nass xls sheet containing mapping data for 'name' and 'sex'
#wc22 = pd.read_csv('WC22_Results.csv', sep=',') # not used... was thinking of merging all WC results also

# Merge the two dataframes on the 'id' column
merged_df = pd.merge(noname_df, name_ids, on='id')

# create year column for grouping purposes
merged_df["date"] = pd.to_datetime(merged_df["date"], infer_datetime_format=True)
merged_df['year'] = merged_df['date'].dt.strftime('%Y')
merged_df['year'] = merged_df['year'].astype(int)

# Mean of 'resultscore'
grouped_df = merged_df.groupby(['id', 'discipline', 'year'])['resultscore'].transform('mean')
# Add the new column 'season_av' to the original DataFrame
merged_df['season_av'] = grouped_df

# Std of 'resultscore'
grouped_df = merged_df.groupby(['id', 'discipline', 'year'])['resultscore'].transform('std')
# Add the new column 'season_av' to the original DataFrame
merged_df['season_std'] = grouped_df

# Get top 5 largest 'resultscore' for each athlete and discipline
top5 = merged_df.groupby(['id', 'discipline'])['resultscore'].nlargest(5)
# Calculate mean of the top 5 for each athlete and discipline
mean_top5 = top5.groupby(['id', 'discipline']).mean()
# Merge the new DataFrame back with the original
merged_df = merged_df.merge(mean_top5.rename('av_top5'), on=['id', 'discipline'], how='left')

# Get top 3 largest 'resultscore' for each athlete and discipline in a season
top3 = merged_df.groupby(['id', 'discipline', 'year'])['resultscore'].nlargest(3)
mean_top3 = top3.groupby(['id', 'discipline', 'year']).mean()
# Merge back with the original
merged_df = merged_df.merge(mean_top3.rename('season_av_top3'), on=['id', 'discipline', 'year'], how='left')


# Mapping 'disciplineCode' to 'discipline'
def assign_discipline_code(row):
    if row['discipline'] == '100 Metres':
        return '100m'
    if row['discipline'] == '100 Metres Hurdles':
        return '100H'
    if row['discipline'] == '110 Metres Hurdles':
        return '110H'
    if row['discipline'] == '200 Metres':
        return '200M'
    if row['discipline'] == '400 Metres':
        return '400M'
    if row['discipline'] == '400 Metres Hurdles':
        return '200H'
    if row['discipline'] == '800 Metres':
        return '800M'
    if row['discipline'] == '1000 Metres':
        return '1k'
    if row['discipline'] == '1500 Metres':
        return '1500M'
    if row['discipline'] == '2000 Metres':
        return '2k'
    if row['discipline'] == '5000 Metres':
        return '5k'
    if row['discipline'] == '10000 Metres':
        return '10k'
    if row['discipline'] == 'Mile':
        return 'Mile'
    if row['discipline'] == '3000 Metres':
        return '3k'
    if row['discipline'] == '3000 Metres Steeplechase':
        return '3kSC'
    if row['discipline'] == '2000 Metres Steeplechase':
        return '2kSC'
    if row['discipline'] == 'Javelin Throw':
        return 'JT'
    if row['discipline'] == 'Hammer Throw':
        return 'HT'
    if row['discipline'] == 'Shot Put':
        return 'SP'
    if row['discipline'] == 'Discus Throw':
        return 'DT'
    if row['discipline'] == 'Long Jump':
        return 'LJ'
    if row['discipline'] == 'High Jump':
        return 'HJ'
    if row['discipline'] == 'Triple Jump':
        return 'TJ'
    if row['discipline'] == 'Pole Vault':
        return 'PV'
    if row['discipline'] == 'Decathlon':
        return 'X10'
    if row['discipline'] == 'Heptathlon':
        return 'X7'
    if row['discipline'] == 'Marathon':
        return 'Marathon'
    if row['discipline'] == '10 Kilometres Race Walk':
        return '10k Walk'
    if row['discipline'] == '15 Kilometres Race Walk':
        return '15k Walk'
    if row['discipline'] == '20 Kilometres Race Walk':
        return '20k Walk'
    if row['discipline'] == '35 Kilometres Race Walk':
        return '35k Walk'
    if row['discipline'] == '50 Kilometres Race Walk':
        return '50k Walk'
    return row['discipline']  # Default return if no condition is met

# Apply the function to each row in the dataframe
merged_df['disciplineCode'] = merged_df.apply(assign_discipline_code, axis=1)

#################################
# need to fetch results for major champs 8th place in discipline then add to column in main df
# used for calculating likelihood of making top 8
#################################


# Print the updated dataframe
print(merged_df)

# comment in and out as needed in preparation of writing
merged_df.to_csv("Athlete_Cleansed2023.csv", mode='w', index=False, sep='|')
