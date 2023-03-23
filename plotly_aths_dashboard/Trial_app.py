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
mytitle = dcc.Markdown(children='# Australian Athletics Analytics')
mygraph = dcc.Graph(id='mygraph', figure={})
mapgraph = dcc.Graph(id='mapgraph', figure={})
sngraph = dcc.Graph(id='sngraph', figure={})
dropdown = dcc.Dropdown(options=df['id'].unique(),
                        value='14550669',  # initial value displayed when page first loads
                        clearable=False, style={'color': 'Black'},
                        searchable=True)

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
        dbc.Col([sngraph], width=6)
    ]),
    dbc.Row([
        dbc.Col([mapgraph], width=6)
    ], justify='left'),

], fluid=True)

##########################################################
# Callback allows components to interact
@app.callback(
    Output(component_id='mygraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    print(user_input)
    #print(df[df['id']==user_input])
    fig = px.scatter(df[df['id']==user_input], x="date", y="resultscore",
                     color="disciplineCode", hover_data=["category", "place", "mark", "wind"],
                     title="Event Results - Hover for more data!")
    fig.update_layout(legend_title_text='')
    return fig  # returned objects are assigned to the component property of the Output


@app.callback(
    Output(component_id='sngraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_sngraph(user_input):
    dfb = df[df['id']==user_input]  # data we're working with is all rows related to 'user_input'
    # add column for season
    dfb['season'] = dfb['date'].dt.strftime('%Y')
    dfb['season'] = dfb['season'].astype(int)  # change the data type so x axis is continuous
    # add column for season best result
    dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')
    fig3 = px.line(dfb, x="season", y="sn_best", color="disciplineCode", markers=True,
                   title="Season's bests")
    fig3.update_layout(legend_title_text='')

    return fig3


@app.callback(
    Output(component_id='mapgraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_mapgraph(user_input):  # function arguments come from the component property of the Input
    print(user_input)
    dff = df[df['id']==user_input]
    dff['count'] = dff.groupby(['country'])['__typename'].transform('count')
    fig2 = px.scatter_geo(dff, locations="country", color="country",
                          size='count', projection="orthographic",
                          title='Competition Travel Footprint')
    fig2.update_traces(marker=dict(line=dict(width=2, color='Blue')), selector=dict(mode='markers'))
    fig2.update_traces(marker_sizemin=5, selector=dict(mode='markers'))

    return fig2  # returned objects are assigned to the component property of the Output



# Run app
if __name__=='__main__':
    app.run_server(port=8053)
