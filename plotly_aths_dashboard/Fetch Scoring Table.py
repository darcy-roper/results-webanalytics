import pandas as pd
import requests

# URL of the JSON file
url = 'https://raw.githubusercontent.com/jchen1/iaaf-scoring-tables/master/iaaf.json'

# Send a GET request to the URL
response = requests.get(url)

# Load the JSON content from the response
data = response.json()

# Convert the JSON data directly to a DataFrame
df = pd.DataFrame(data)

# Convert the DataFrame to a CSV file
csv_file_path = 'iaaf_scoring_tables.csv'
df.to_csv(csv_file_path, index=False)

print(f'Data saved to {csv_file_path}')
