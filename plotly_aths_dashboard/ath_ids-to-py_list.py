# convert text file ath_ids into a text list
import numpy as np

with open("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/ath_ids.txt", 'r') as f:
    data = f.read()
    ff = str.split(data)
    print(ff)
