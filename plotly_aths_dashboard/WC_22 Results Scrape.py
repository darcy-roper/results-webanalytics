

# event_options = [
#     '10229509', '10229510', '10229511', '10229512', '10229513',
#     '10229514', '10229521', '10229522', '10229523', '10229524',
#     '10229526', '10229527', '10229528', '10229529', '10229530',
#     '10229531', '10229532', '10229533', '10229534', '10229535',
#     '10229989', '10229536', '10229630',
#     '10229605', '10229631', '10229501', '10229502', '10229609',
#     '10229610', '10229611', '10229612', '10229614', '10229615',
#     '10229616', '10229617', '10229618', '10229619', '10229620',
#     '10229621', '10229636', '10229634', '10229508', '10229627',
#     '10229629']

import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = 'https://worldathletics.org/competition/calendar-results/results/7137279?eventId=10229511'

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element using XPath
table_xpath = '//*[@id="__next"]/article/div[2]/section/div[1]/span/strong'
table_element = soup.find('strong', {'xpath': table_xpath}).find_next('table')

# Extract the table headers
headers = [th.text for th in table_element.find('thead').find_all('th')]

# Extract the table rows
rows = []
for tr in table_element.find('tbody').find_all('tr'):
    row = [td.text for td in tr.find_all('td')]
    rows.append(row)

# Extract the desired information from each row
results = []
for row in rows:
    result = {
        'Place': row[0],
        'Name': row[1],
        'NAT': row[2],
        'Mark': row[3]
    }
    results.append(result)

# Print the extracted results
for result in results:
    print(result)
