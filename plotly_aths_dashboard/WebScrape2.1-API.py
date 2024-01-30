# Using hidden API to obtain results data
# Create variables such as Year and athlete ID to iterate through athletes
import csv

import requests
import json
import pandas as pd

# create an empty csv with headers to append athlete data into
df = pd.DataFrame({'id': [], 'date': [], 'competition': [], 'venue': [], 'indoor': [], 'disciplineCode': [], 'disciplineNameUrlSlug': [], 'typeNameUrlSlug': [], 'discipline': [], 'country': [], 'category': [], 'race': [], 'place': [], 'mark': [], 'wind': [], 'notlegal': [], 'resultscore': [], 'remark': [], '__typename': []})
df.to_csv('Athlete_Raw2023.csv', mode='w', index=False, sep='|')

url = 'https://5uw5qolq5ff7bndkrvrpeyfc3m.appsync-api.eu-west-1.amazonaws.com/graphql'

ath_id = [
    '14336705', '14407592', '14411267', '14464527', '14565327', '14673644', '14457807', '14455361',
    '14456885', '14271241', '14940604', '14436890', '14446988', '14272002', '14667553', '14464506',
    '14500488', '14271632', '14387190', '14619618', '14572123', '14743991', '14464502', '14463325',
    '14575440', '14636659', '14455195', '14517121', '14613323', '14622158', '14511251', '14490253',
    '14731617', '14575462', '14179673', '14533629', '14549778', '14636668', '14820122', '14365887',
    '14671089', '14874649', '14778459', '14924344', '14552175', '14690008', '14767186', '14550669',
    '14611740', '14271094', '14336656', '14436876', '14496696', '14740976', '14787531', '14608674',
    '14271807', '14671065', '14817316', '14970569', '14674731', '14761633', '14861747', '14622433',
    '14777855', '14555113', '14765468', '14448453', '14691030', '14865727', '14812769', '14815270',
    '14859206', '14823682', '14668498', '14730466', '14878490', '14861699', '14935280', '14615310',
    '14769953', '14733124', '14861366', '14861460', '14670290', '14922448', '14691224', '14861793',
    '14831970', '14814102', '14875656', '14812564', '14636671', '14771862', '14774575', '14831958',
    '14828239', '14815259', '14962470', '14814142', '14686671', '14689526', '14782478', '14963397',
    '14861516', '14861525', '14577424', '14519260', '14360445', '14768392', '14411012', '14406120',
    '14336764', '14689546', '14517594', '14272049', '14553618', '14495639', '14619610', '14411163',
    '14554579', '14635855', '14496066', '14517173', '14576384', '14517160', '14336706', '14386314',
    '14433154', '14668477'
]
# variable containing all 2023/24 NASS athletes on AA website


while True:
    for athlete in ath_id:
        item = athlete
        results = []  # empty list to paste in results when iterating through 'results in data...' for loop
        for year in range(2012, 2024):  # for loop to extract only data from 2012-2023 (2024 is not included in range)
            try:
                payload = json.dumps({
                  "operationName": "GetSingleCompetitorResultsDate",
                  "variables": {
                    "resultsByYear": year,
                    "resultsByYearOrderBy": "date",
                    "id": item
                  },
                  "query": "query GetSingleCompetitorResultsDate($id: Int, $resultsByYearOrderBy: String, $resultsByYear: Int) {\n  getSingleCompetitorResultsDate(id: $id, resultsByYear: $resultsByYear, resultsByYearOrderBy: $resultsByYearOrderBy) {\n    parameters {\n      resultsByYear\n      resultsByYearOrderBy\n      __typename\n    }\n    activeYears\n    resultsByDate {\n      date\n      competition\n      venue\n      indoor\n      disciplineCode\n      disciplineNameUrlSlug\n      typeNameUrlSlug\n      discipline\n      country\n      category\n      race\n      place\n      mark\n      wind\n      notLegal\n      resultScore\n      remark\n      __typename\n    }\n    __typename\n  }\n}\n"
                })
                headers = {
                  'authority': '5uw5qolq5ff7bndkrvrpeyfc3m.appsync-api.eu-west-1.amazonaws.com',  # edit from cURL
                  'accept': '*/*',
                  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                  'content-type': 'application/json',
                  'origin': 'https://worldathletics.org',
                  'referer': 'https://worldathletics.org/',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'cross-site',
                  'sec-gpc': '1',
                  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                  'x-amz-user-agent': 'aws-amplify/3.0.2',
                  'x-api-key': 'da2-5lvtzjfp5bfrrifgztn4jlbn7y'  # edit from cURL
                }  # collapse headers with user information to provide world athletics server through API

                response = requests.request("POST", url, headers=headers, data=payload)  # use 'request' interpreter to concatenate above variables from API
                print(response.text)  # tracks progress in terminal
                data = response.json()

                for result in data["data"]["getSingleCompetitorResultsDate"]["resultsByDate"]:  # goes down each key phrase in json
                    results.append(result)
                    res_data = pd.json_normalize(result)  # convert json to structured dataframe columns
                    res_data.insert(0, "id", item, True)  # inserts athlete id into dataframe at column 0
                    res_data.to_csv("Athlete_Raw2023.csv", mode='a', index=False, header=False, sep='|')  # change csv file path to create new copy
            except TypeError:
                year = year + 1

    break

pandas_file = pd.read_csv('Athlete_Raw2023.csv', sep='|')
print(pandas_file)
