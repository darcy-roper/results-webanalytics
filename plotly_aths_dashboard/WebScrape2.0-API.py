# Using hidden API to obtain results data
# Create variables such as Year and athlete ID to iterate through athletes

import requests
import json
import pandas as pd

url = "https://txhj5c3pafc57aflonu6rhxtxu.appsync-api.eu-west-1.amazonaws.com/graphql"

ath_id = ["14550669", "14336705", "14455361",]  # variable for the athlete id

while True:
    for athlete in ath_id:
        item = athlete
        #results = []  # empty list to paste in results when iterating through 'results in data...' for loop
        for year in range(2012, 2023):  # for loop to extract only data from 2012-2022 (2023 is not included in range)
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
                  'authority': 'txhj5c3pafc57aflonu6rhxtxu.appsync-api.eu-west-1.amazonaws.com',
                  'accept': '*/*',
                  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                  'content-type': 'application/json',
                  'origin': 'https://worldathletics.org',
                  'referer': 'https://worldathletics.org/',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'cross-site',
                  'sec-gpc': '1',
                  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
                  'x-amz-user-agent': 'aws-amplify/3.0.2',
                  'x-api-key': 'da2-u2ciortsnrdxxcsr27sjqtx4qe'
                }  # collapse headers with user information to provide world athletics server through API

                response = requests.request("POST", url, headers=headers, data=payload)  # use 'request' interpreter to concatenate above variables from API
                print(response.text)  # tracks progress in terminal

                data = response.json()
                for result in data["data"]["getSingleCompetitorResultsDate"]["resultsByDate"]:  # goes down each key phrase in json
                    #results.append(result)
                    res_data = pd.json_normalize(result)  # convert json to structured dataframe columns
                    res_data.insert(0, "id", item, True)  # inserts athlete id into dataframe at column 0
                    res_data.to_csv("Athlete-results.csv", mode='a', header=False, index=False)
            except TypeError:
                year = year + 1


    break
