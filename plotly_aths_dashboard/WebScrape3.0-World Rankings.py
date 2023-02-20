# Using hidden API to obtain toplist data
# wanting to scrape all <td> HTML elements
# !!!!ATTENTION!!! - known data quality issue for athletes with no DOB the row data will be out of alignment
# to resolve the DOB issue any athlete with no known DOB will be removed from the lists in Alteryx data cleanse

import requests
import pandas as pd

# list of all events to write into URL and file names (adapt this for male events)
events = ["100m", "200m", "400m", "800m", "1500m", "5000m", "10000m", "100mh", "400mh",
          "3000msc", "high-jump", "long-jump", "pole-vault", "triple-jump", "shot-put",
          "discus-throw", "hammer-throw", "javelin-throw", "road-running", "marathon",
          "race-walking", "35km-race-walking", "heptathlon"]

for event in events:
    # open request with URL
    from requests_html import HTMLSession
    url = "https://worldathletics.org/world-rankings/"+event+"/women?regionType=world&page=1&rankDate=2022-12-27&limitByCountry=0"

    # commence HTML session
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    ###########################
    # scrape data from response
    # create variable from CSS class
    tabledata = response.html.find('.table-row--hover')
    worldranks = []
    for i in range(len(tabledata)):
        x = tabledata[i].text
        worldranks.append(x)
    ###########################

    ###########################
    # Create and transform dataframe
    # this splits list items in worldranks into pandas df
    df = pd.DataFrame({'col1': [worldranks]})
    for item in worldranks:
        df.loc[len(df)] = item
    df = df.drop(0)  # removed the first row as reference row

    # replace all \n with |
    df2 = df.replace('\n', '|', regex=True)

    # split out data into new columns
    df[['Rank', 'Name', 'DOB', 'Country', 'Score', 'Discipline']] = df2['col1'].str.split("|", expand=True)
    df3 = df.drop('col1', axis='columns') # remove reference column
    print(df3)
    ###########################

    df3.to_csv("2022 World Rankings/F_"+event+".csv", mode='w', header=False, index=False)
