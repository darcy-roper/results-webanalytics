# File to join by athlete id using pandas
# This program also performs statistical analysis on the data frame

import pandas as pd
import statsmodels.api as sm

#read csvs
noname_df = pd.read_csv('somethingNew.csv', sep='|')
name_ids = pd.read_csv('NASS list (20-21).csv', sep=',')
# the nass list csv was extracted from the nass xls sheet containing mapping data for 'name' and 'sex'
wc22 = pd.read_csv('WC22_Results.csv', sep=',')

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

# need to fetch results for major champs 8th place in discipline then add to column in main df
# used for calculating likelihood of making top 8


# Print the updated dataframe
print(merged_df)


# merged_df.to_csv("Dataframe_Analysis.csv", mode='w', index=False, sep='|')
