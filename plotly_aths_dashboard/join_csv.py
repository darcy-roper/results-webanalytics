# File to join by athlete id using pandas

import pandas as pd

noname_df = pd.read_csv('somethingNew.csv', sep='|')
name_ids = pd.read_csv('NASS list (20-21).csv', sep=',')

# Merge the two dataframes on the 'id' column
merged_df = pd.merge(noname_df, name_ids, on='id')

# Print the merged dataframe
print(merged_df)
