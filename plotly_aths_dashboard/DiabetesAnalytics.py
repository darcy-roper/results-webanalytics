# machine learning model to accurately predict
# whether patients in the dataset have diabetes or not


import pandas as pd
import pandas_profiling as pp

df = pandas.read_csv('Datasets/diabetes.csv')
pp = pandas_profiling(df)
print(pp)
