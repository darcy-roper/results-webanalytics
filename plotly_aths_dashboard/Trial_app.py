import dash
from dash import dcc, Output, Input, Dash
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import date

df = pd.read_csv('somethingNew.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
#print(df.head())

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
mytitle = dcc.Markdown(children='# Results')
mygraph = dcc.Graph(id='mygraph', figure={})
mapgraph = dcc.Graph(id='mapgraph', figure={})
dropdown = dcc.Dropdown(options=df['id'].unique(),
                        value='14550669',  # initial value displayed when page first loads
                        clearable=False, style={'color': 'Black'})

# Customize Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=6),
        dbc.Col([mapgraph], width=6)
    ]),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(component_id='mygraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    print(user_input)
    #print(df[df['id']==user_input])
    fig = px.scatter(df[df['id']==user_input], x="date", y="resultscore", color="discipline", hover_data=["category", "place", "mark", "wind"])

    return fig  # returned objects are assigned to the component property of the Output

##########################################################
# 2nd Callback for map
@app.callback(
    Output(component_id='mapgraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_mapgraph(user_input):  # function arguments come from the component property of the Input
    print(user_input)
    dff = df[df['id']==user_input]
    dff['count'] = dff.groupby(['country'])['__typename'].transform('count')
    fig2 = px.scatter_geo(dff, locations="country", color="country",
                          size='count', projection="orthographic")
    fig2.update_traces(marker=dict(line=dict(width=2, color='Blue')), selector=dict(mode='markers'))
    fig2.update_traces(marker_sizemin=5, selector=dict(mode='markers'))

    return fig2  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8053)
