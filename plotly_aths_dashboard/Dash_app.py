# this program will form the page view when only considering 1 athletes' data
# use 'test_app.py' for page 2 which will compare 2 athletes
import dash
from dash import dcc, Dash, dash_table, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


df = pd.read_csv('Dataframe_Analysis.csv', sep='|')  # updated csv following statistical calcs in 'join_csv.py'
dff = pd.read_csv('Datasets/WC22_Results.csv', sep=',')  # result data from Oregon WC 2022
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)


# Figure components
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
mytitle = dcc.Markdown(children='# Australian Athletics Analytics')
mygraph = dcc.Graph(id='mygraph', figure={})
mapgraph = dcc.Graph(id='mapgraph', figure={})
sngraph = dcc.Graph(id='sngraph', figure={})
placegraph = dcc.Graph(id='placegraph', figure={})
cat_placing = dcc.Graph(id='graph_placing', figure={})
year_prog_graph = dcc.Graph(id='year_prog_graph', figure={})


# format unique dropdown options
unique_names = df['name'].unique()  # unique values from name column
# create dropdown options using unique names
dropdown_options = [{'label': name, 'value': id} for id, name in zip(df['id'].unique(), unique_names)]
dropdown = dcc.Dropdown(options=dropdown_options,
                        value='14336705',  # initial value displayed when page first loads
                        clearable=False, style={'color': 'Black'}, searchable=True)
event_select = dcc.Dropdown(
    id='event_sel',
    options=[{'label': i, 'value': i} for i in df['discipline'].unique()],
    value=[],
    multi=True,
    style={'color': 'Black'})

# Creating & formatting options for the checklist of competition categories
# Add the "select-all" option to the options list
options = [{'label': i, 'value': i} for i in df['category'].dropna().unique()]
options.append({'label': 'Select All', 'value': 'select-all'})
options.append({'label': 'Deselect All', 'value': 'deselect-all'})
options = [{'label': 'F', 'value': 'F', 'order': 1},
           {'label': 'E', 'value': 'E', 'order': 2},
           {'label': 'D', 'value': 'D', 'order': 3},
           {'label': 'C', 'value': 'C', 'order': 4},
           {'label': 'B', 'value': 'B', 'order': 5},
           {'label': 'A', 'value': 'A', 'order': 6},
           {'label': 'GL', 'value': 'GL', 'order': 7},
           {'label': 'GW', 'value': 'GW', 'order': 8},
           {'label': 'DF', 'value': 'DF', 'order': 9},
           {'label': 'OW', 'value': 'OW', 'order': 10},
           {'label': 'Select All', 'value': 'select-all', 'order': 11},
           {'label': 'Deselect All', 'value': 'deselect-all', 'order': 12}]  # orders the options according to the list
options = sorted(options, key=lambda x: x['order'])
# Get all available category options
category_options = [option['value'] for option in options if option['value'] not in ['select-all', 'deselect-all']]
catradio = dbc.Checklist(
    id='catradio',
    options=options,
    value=category_options,
    inline=True,
    labelStyle={'display': 'inline-block', 'margin-right': '10px'})



# Creating a dbc.Card for catradio and cat_placing
cat_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([catradio], width=12),
                ]),
                dbc.Row([
                    dbc.Col([cat_placing], width=12)
                ]),
            ]
        ),
    ],
)

# Customize Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            dropdown,
            event_select,
            #key_stats_card,
        ], width=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([mygraph], width=12),
            ], justify='end'),
            dbc.Row([
                dbc.Col([sngraph], width=12),
            ], justify='end'),
            dbc.Row([
                dbc.Col([mapgraph], width=6),
                dbc.Col([placegraph], width=6)
            ], justify='end'),
            dbc.Row([
                dbc.Col([cat_card], width=12),
            ], justify='end'),
            dbc.Row([
                dbc.Col([year_prog_graph], width=12),
            ], justify='end'),
        ], width=9),
    ]),
], fluid=True)

# Callbacks for handling both inputs from the user
@app.callback(
    Output(component_id='event_sel', component_property='options'),
    Input(dropdown, component_property='value'))
def get_event_options(user_input):
    df0 = df[df['id'] == user_input]
    return [{'label': i, 'value': i} for i in df0['discipline'].unique()]

@app.callback(
    Output(component_id='event_sel', component_property='value'),
    Input(component_id='event_sel', component_property='options'))
def get_event_value(event_sel):
    if event_sel:
        values = [k['value'] for k in event_sel]
        counts = {value: values.count(value) for value in values}
        default_value = max(counts, key=counts.get)
        return default_value

# Update all main graphs (except for the pie graphs for placing)
@app.callback(
    [Output(component_id='mygraph', component_property='figure'),
     Output(component_id='sngraph', component_property='figure'),
     Output(component_id='mapgraph', component_property='figure'),
     Output(component_id='placegraph', component_property='figure'),
     Output(component_id='year_prog_graph', component_property='figure')],
    [Input(dropdown, component_property='value'),
     Input('event_sel', 'value')]
)
def update_all_graphs(user_input, event_select1):
    if not event_select1:
        filtered_data = df.loc[df['id'] == user_input]
    else:
        if isinstance(event_select1, str):
            event_select1 = [event_select1]
        filtered_data = df.loc[(df['id'] == user_input) & (df['discipline'].isin(event_select1))]

    # update mygraph
    fig = px.scatter(filtered_data, x="date", y="resultscore",
                     color="disciplineCode", hover_data=["category", "place", "mark", "wind"],
                     title="Event Results - Hover for more information!")
    fig.update_layout(legend_title_text='')

    # update sngraph
    dfb = filtered_data.copy()
    dfb['season'] = dfb['date'].dt.strftime('%Y')
    dfb['season'] = dfb['season'].astype(int)
    dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')
    fig3 = px.line(dfb, x="season", y="sn_best", color="disciplineCode", markers=True,
                   title="Season's bests")
    fig3.update_layout(legend_title_text='')

    # trends in each year
    dfc = filtered_data.copy()
    dfc['year'] = dfc['date'].dt.strftime('%Y')
    dfc['year'] = dfc['year'].astype(int)
    fig6 = px.scatter(dfc, x="date", y="resultscore",
                  color="discipline", hover_data=["category", "place", "mark", "wind"],
                  title="Season rates of progression")
    # Add trend lines for each year
    for year in dfc['year'].unique():
        group = dfc[dfc['year'] == year]
        trendline_ols = px.scatter(group, x="date", y="resultscore", trendline="ols").data[1]
        trendline_ols['line']['color'] = 'red'  # Set color of trendline_ols to red
        trendline_lowess = px.scatter(group, x="date", y="resultscore", trendline="lowess").data[1]
        trendline_lowess['line']['color'] = 'blue'  # Set color of trendline_lowess to blue
        fig6.add_trace(trendline_ols)
        fig6.add_trace(trendline_lowess)
    fig6.update_layout(legend_title_text='')

    # update mapgraph
    dff = filtered_data.copy()
    dff['count'] = dff.groupby(['country'])['__typename'].transform('count')
    fig2 = px.scatter_geo(dff, locations="country", color="country",
                          size='count', projection="orthographic",
                          title='Competition Travel Footprint')
    fig2.update_traces(marker=dict(line=dict(width=2, color='Blue')), selector=dict(mode='markers'))
    fig2.update_traces(marker_sizemin=5, selector=dict(mode='markers'))

    # update placegraph
    dfa = filtered_data.copy()
    hovertemp1 = "<b>Category: </b> %{label} <br>"
    hovertemp1 += "<b>Number of appearances: </b> %{value}"
    dfa1 = dfa.groupby(['place', 'category']).size().reset_index(name='number_of_placings')  # apply grouping to count number of comp appearances
    fig4 = px.pie(dfa1, values='number_of_placings', names='category', title='Competition appearances by meet category',
                  color='category', color_discrete_map={'A': 'gold', 'B': 'silver', 'C': 'saddlebrown'})
    fig4.update_traces(hovertemplate=hovertemp1)

    # update key stats figures
    dfd = filtered_data.copy()


    return fig, fig3, fig2, fig4, fig6

# Trial for dynamic pie graph based on 3rd dropdown selection for category
# Add a callback to set the value of the catradio component to all options' values
@app.callback(
    Output('catradio', 'value'),
    Input('catradio', 'options'),
    Input('catradio', 'value'))
def select_all_options(options, values):
    if 'select-all' in values:
        return [x['value'] for x in options if x['value'] != 'select-all']
    elif 'deselect-all' in values:
        return []
    else:
        return values

@app.callback(
    Output(component_id='graph_placing', component_property='figure'),
    Input(component_id='catradio', component_property='value'),
    Input(dropdown, component_property='value'),
    Input('event_sel', 'value'))
def update_pie_graph(catradio_value, dropdown_value, event_sel_value):
    if not catradio_value or not dropdown_value:
        return {}
    if not event_sel_value:
        filtered_data = df.loc[(df['id'] == dropdown_value) & (df['category'].isin(catradio_value)) & (df['race'] == 'F')]
    else:
        if isinstance(event_sel_value, str):
            event_sel_value = [event_sel_value]
        filtered_data = df.loc[(df['id'] == dropdown_value) & (df['category'].isin(catradio_value)) & (df['discipline'].isin(event_sel_value)) & (df['race'] == 'F')]

    filtered_data1 = filtered_data.groupby(['place', 'category']).size().reset_index(name='number_of_placings')
    fig5 = px.histogram(filtered_data1, y='number_of_placings', x='place', color='place', color_discrete_sequence=px.colors.sequential.algae,
                        color_discrete_map={'1.': 'gold', '2.': 'silver', '3.': 'saddlebrown'},
                        category_orders={'place': ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.']})
    fig5.update_layout(title="Placing by category (Finals only)")
    return fig5


# Run app
if __name__ == '__main__':
    app.run_server(port=8053)
