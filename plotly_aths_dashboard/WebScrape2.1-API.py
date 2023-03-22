# Using hidden API to obtain results data
# Create variables such as Year and athlete ID to iterate through athletes

import requests
import json
import pandas as pd

url = 'https://2mlp5vgc7ffwlb763jx7yrizqu.appsync-api.eu-west-1.amazonaws.com/graphql'

ath_id = ['14336705', '14455361']
# variable containing all 2021 NASS athletes on AA website


# athlete ids: total 117 athletes
# ['14336705', '14455361', '14673644', '14456885', '14940604', '14436890', '14272002', '14407592',
#           '14464527', '14565327', '14500488', '14271632', '14457807', '14411267', '14387190', '14271241',
#           '14463325', '14575440', '14455195', '14613323', '14490253', '14446988', '14617484', '14667553',
#           '14464506', '14550669', '14433154', '14619618', '14436876', '14765461', '14271807', '14831970',
#           '14514627', '14411273', '14768392', '14517121', '14634207', '14636668', '14674731', '14761633',
#           '14622433', '14555113', '14764890', '14517181', '14448453', '14576384', '14517160', '14611740',
#           '14732754', '14673646', '14636659', '14733182', '14615310', '14769938', '14731742', '14730127',
#           '14787531', '14730464', '14769953', '14861366', '14609656', '14820122', '14691224', '14861747',
#           '14812564', '14636671', '14777855', '14774575', '14765468', '14814142', '14727709', '14689526',
#           '14865727', '14815270', '14859206', '14576087', '14861525', '14668498', '14730466', '14733176',
#           '14519260', '14360445', '14496696', '14272435', '14411012', '14406120', '14336764', '14445318',
#           '14689546', '14517594', '14731617', '14471777', '14608674', '14554575', '14179673', '14272049',
#           '14533629', '14549778', '14553618', '14384288', '14495639', '14514622', '14411163', '14924344',
#           '14496066', '14552175', '14271509', '14517173', '14727680', '14336706', '14370966', '14386314',
#           '14336656', '14668477', '14271094', '14271451', '14496063']


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
                  'authority': '2mlp5vgc7ffwlb763jx7yrizqu.appsync-api.eu-west-1.amazonaws.com',  # edit from cURL
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
                  'x-api-key': 'da2-k4nwfju55bazhfisjzetwm4ove'  # edit from cURL
                }  # collapse headers with user information to provide world athletics server through API

                response = requests.request("POST", url, headers=headers, data=payload)  # use 'request' interpreter to concatenate above variables from API
                print(response.text)  # tracks progress in terminal

                data = response.json()
                for result in data["data"]["getSingleCompetitorResultsDate"]["resultsByDate"]:  # goes down each key phrase in json
                    #results.append(result)
                    res_data = pd.json_normalize(result)  # convert json to structured dataframe columns
                    res_data.insert(0, "id", item, True)  # inserts athlete id into dataframe at column 0
                    res_data.to_csv("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/DF_Headers.csv",
                                    mode='w',
                                    headers=True,
                                    # columns=['id', 'date', 'competition', 'venue', 'indoor', 'disciplineCode', 'disciplineNameUrlSlug', 'typeNameUrlSlug', 'discipline', 'country', 'category', 'race', 'place', 'mark', 'wind', 'notlegal', 'resultscore', 'remark', '__typename'],
                                    # header=['id', 'date', 'competition', 'venue', 'indoor', 'disciplineCode', 'disciplineNameUrlSlug', 'typeNameUrlSlug', 'discipline', 'country', 'category', 'race', 'place', 'mark', 'wind', 'notlegal', 'resultscore', 'remark', '__typename'],
                                    index=False)  # change csv file path to create new copy
            except TypeError:
                year = year + 1

    break
