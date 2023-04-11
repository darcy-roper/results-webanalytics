import dash
from dash import dcc, Output, Input, Dash, ctx
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
placegraph = dcc.Graph(id='placegraph', figure={})
piegraph_placing = dcc.Graph(id='piegraph_placing', figure={})
year_prog_graph = dcc.Graph(id='year_prog_graph', figure={})

dropdown = dcc.Dropdown(options=df['id'].unique(),
                        value='14550669',  # initial value displayed when page first loads
                        clearable=False, style={'color': 'Black'},
                        searchable=True)

event_select = dcc.Dropdown(id='event_sel',
                            options=[],
                            style={'color': 'Black'},
                            multi=True)

# Customize Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown], width=6),
        dbc.Col([event_select], width=6),
    ]),
    dbc.Row([
        dbc.Col([mygraph], width=6),
        dbc.Col([sngraph], width=6)
    ]),
    dbc.Row([
        dbc.Col([piegraph_placing], width=4),
        dbc.Col([placegraph], width=4),
        dbc.Col([mapgraph], width=4)
    ]),
    dbc.Row([
        ###
    ], justify='center'),

], fluid=True)

#####_____________multi dropdown callbacks____________####
@app.callback(
    Output(component_id='event_sel', component_property='options'),
    Input(dropdown, component_property='value'))
def get_event_options(user_input):
    df0 = df[df['id'] == user_input]
    return [{'label': i, 'value': i} for i in df0['discipline'].unique()]

@app.callback(
    Output(component_id='event_sel', component_property='value'),
    Input(component_id='event_sel', component_property='options'))
def get_event_value(event_sel):  # function arguments come from the component property of the Input
    return [k['value'] for k in event_sel][1]


#####__________________________________________________####
@app.callback(
    Output(component_id='mygraph', component_property='figure'),
    Input(dropdown, component_property='value'),
    Input(event_select, component_property='value'))
def update_graph(user_input, event_select1):
    if not event_select1:
        filtered_data = df.loc[df['id'] == user_input]
    else:
        filtered_data = df.loc[(df['id'] == user_input) & (df['discipline'].isin(event_select1))]
    fig = px.scatter(filtered_data, x="date", y="resultscore",
                     color="discipline", hover_data=["category", "place", "mark", "wind"],
                     title="Event Results - Hover for more data!")
    fig.update_layout(legend_title_text='')
    return fig

#filtering the season to add traces for season trendlines
@app.callback(
    Output(component_id='year_prog_graph', component_property='figure'),
    Input(dropdown, component_property='value'),
    Input(event_select, component_property='value'))
def update_trend_graph(user_input, event_select1):
    if not event_select1:
        filtered_data = df.loc[df['id'] == user_input]
    else:
        filtered_data = df.loc[(df['id'] == user_input) & (df['discipline'].isin(event_select1))]
    filtered_data['year'] = filtered_data['date'].dt.strftime('%Y')
    filtered_data['year'] = filtered_data['year'].astype(int)
    fig6 = px.scatter(filtered_data, x="year", y="resultscore",
                      color="discipline", hover_data=["category", "place", "mark", "wind"],
                      trendline="ols", facet_col="year",
                      title="Season Rates of progression")
    fig6.update_layout(legend_title_text='')
    return fig6

@app.callback(
    Output(component_id='sngraph', component_property='figure'),
    Input(dropdown, component_property='value'))
def update_sngraph(user_input):
    dfb = df[df['id'] == user_input]  # data we're working with is all rows related to 'user_input'
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
    #print(user_input)
    dff = df[df['id'] == user_input]
    dff['count'] = dff.groupby(['country'])['__typename'].transform('count')
    fig2 = px.scatter_geo(dff, locations="country", color="country",
                          size='count', projection="orthographic",
                          title='Competition Travel Footprint')
    fig2.update_traces(marker=dict(line=dict(width=2, color='Blue')), selector=dict(mode='markers'))
    fig2.update_traces(marker_sizemin=5, selector=dict(mode='markers'))

    return fig2  # returned objects are assigned to the component property of the Output


@app.callback(
    Output(component_id='placegraph', component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_placegraph(user_input):  # function arguments come from the component property of the Input
    dfa = df[df['id'] == user_input]
    #dfa['num_place'] = dfa.groupby(['category', 'place'])['place'].transform('count')
    hovertemp1 = "<b>Category: </b> %{label} <br>"  # format the hover labels
    hovertemp1 += "<b>Number of placings: </b> %{value}"  # format hover labels
    fig4 = px.pie(dfa, values='place', names='category', title='Competitions by Category - Click on different sections of the pie!',
                  color='category', color_discrete_map={'A': 'gold', 'B': 'silver', 'C': 'saddlebrown'})
    fig4.update_traces(hovertemplate=hovertemp1)

    return fig4  # returned objects are assigned to the component property of the Output

######### interactive hover for placing at various category meets #########

@app.callback(
    Output(component_id='piegraph_placing', component_property='figure'),
    Input(component_id='placegraph', component_property='clickData'),
    Input(dropdown, component_property='value'),
)
def update_side_graph(clickData, user_input):
    if clickData is None:
        dff2 = df[df['id'] == user_input]
        abc = dff2.groupby(['place', 'category']).size().reset_index(name='number_of_placings')
        fig5 = px.pie(abc, values='number_of_placings', names='place', title='Placing at all Competitions',
                      color='place', color_discrete_sequence=px.colors.sequential.algae, color_discrete_map={'1.': 'gold', '2.': 'silver', '3.': 'saddlebrown'})
        return fig5
    else:
        print(f'clicked data: {clickData}')
        dff2 = df[df['id'] == user_input]
        abc = dff2.groupby(['place', 'category']).size().reset_index(name='number_of_placings')
        abc['number_of_placings'] = abc['number_of_placings'].astype(int)
        clk_category = clickData['points'][0]['label']
        abc = abc[abc['category'] == clk_category]
        fig5 = px.pie(abc, values='number_of_placings', names='place', title=f'Placing distribution at {clk_category} meets',
                      color='place', color_discrete_sequence=px.colors.sequential.algae, color_discrete_map={'1.': 'gold', '2.': 'silver', '3.': 'saddlebrown'})

        return fig5


# Run app
if __name__=='__main__':
    app.run_server(port=8053)
