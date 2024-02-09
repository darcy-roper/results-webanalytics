
import pandas as pd

# Load the CSV file
df = pd.read_csv('iaaf_scoring_tables.csv')

# Add 'sex' column based on 'gender' column
df['sex'] = df['gender'].apply(lambda x: 'M' if x == 'men' else 'W')

# Reorder columns to insert 'sex' between 'gender' and 'event'
column_order = ['category', 'gender', 'sex', 'event', 'mark', 'points']
df = df[column_order]

# Save the modified DataFrame to a new CSV file
df.to_csv('iaaf_scoring_tables_modified.csv', index=False)

print("CSV file has been modified and saved as 'iaaf_scoring_tables_modified.csv'")

