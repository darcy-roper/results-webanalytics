# machine learning model to accurately predict
# whether patients in the dataset have diabetes or not
# Press ⌘ / to bulk hash out lines


import numpy as np
import pandas as pd
import pandas_profiling as pp
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv("/Users/newmac/PycharmProjects/results-webanalytics/plotly_aths_dashboard/Datasets/diabetes.csv")


#-----------------------------------------------------------#
# profile = pp.ProfileReport(df)
# profile.to_file(output_file="Diabetes dataset profile.html")
# creates report to view analytics in html and check dataset for errors
# hash out section once report successfully created

# After looking at the data we have errors with '0' reporting and therefore should replace 0's with nan.
df2 = df.copy(deep=True)
df2[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = df2[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']].replace(0, np.NaN)
# It's good practice creating a copy of the dataframe (df2) and make changes to the copy


#-----------------------------------------------------------#
# Diabetes Outcome - Pie Chart
fig_pie = px.pie(df2, names=df2['Outcome'].map({1: 'Yes', 0: 'No'}), title='Outcome of Diabetes Diagnosis',
                 color_discrete_sequence=px.colors.sequential.Turbo)
fig_pie.show()
# can select colour scales from examples here https://plotly.com/python/builtin-colorscales


#-----------------------------------------------------------#
# Diabetes Correlation matrix - from 0-1
def df2_to_correlationmatrix(df2):
    return {'z': df2.values.tolist(),
            'x': df2.columns.tolist(),
            'y': df2.index.tolist()}


dfNew = df2.corr()
fig_matrix = go.Figure(data=go.Heatmap(df2_to_correlationmatrix(dfNew)))
fig_matrix.show()


#-----------------------------------------------------------#
# Diabetes scatter plot comparing 2 input variables
fig_scatter = px.scatter(df2, x='Glucose', y='Insulin')
fig_scatter.update_traces(marker_color="turquoise", marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
fig_scatter.update_layout(title_text='Glucose and Insulin - Scatter Plot')
fig_scatter.show()


#-----------------------------------------------------------#
# Diabetes box plot comparing 2 inputs (Age/Outcome)
fig_box = px.box(df2, x=df2['Outcome'].map({1: 'Positive Diagnosis', 0: 'Negative Diagnosis'}), y='Age', title="Box plot analysing Age vs Outcome", points='all')
fig_box.update_xaxes(title_text="Diabetes Diagnosis")  # updates the text displayed on the xaxes because the .map function overwrites the axes label in line above
fig_box.show()


#-----------------------------------------------------------#
# Diabetes box plot comparing 2 inputs (BMI/Outcome)
fig_box2 = px.box(df2, x=df2['Outcome'].map({1: 'Positive Diagnosis', 0: 'Negative Diagnosis'}), y='BMI', title="Box plot analysing BMI vs Outcome", points='all')
fig_box2.update_xaxes(title_text="Diabetes Diagnosis")  # updates the text displayed on the xaxes because the .map function overwrites the axes label in line above
fig_box2.show()
