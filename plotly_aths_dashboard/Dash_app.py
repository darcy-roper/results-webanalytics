import dash
from dash import dcc, Dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv('somethingNew.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)


# Figure components
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
mytitle = dcc.Markdown(children='# Australian Athletics Analytics')
mygraph = dcc.Graph(id='mygraph', figure={})
mapgraph = dcc.Graph(id='mapgraph', figure={})
sngraph = dcc.Graph(id='sngraph', figure={})
placegraph = dcc.Graph(id='placegraph', figure={})
cat_placing = dcc.Graph(id='piegraph_placing', figure={})
dropdown = dcc.Dropdown(options=[{'label': i, 'value': i} for i in df['id'].unique()],
                        value='14550669',  # initial value displayed when page first loads
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
# Get all available category options
category_options = [option['value'] for option in options if option['value'] != 'select-all']
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
        dbc.Col([mapgraph], width=4),
        dbc.Col([placegraph], width=4),
        dbc.Col([cat_card], width=4)
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
     Output(component_id='placegraph', component_property='figure')],
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
    fig4 = px.pie(dfa1, values='number_of_placings', names='category', title='Competition appearances by Category',
                  color='category', color_discrete_map={'A': 'gold', 'B': 'silver', 'C': 'saddlebrown'})
    fig4.update_traces(hovertemplate=hovertemp1)

    return fig, fig3, fig2, fig4

# Trial for dynamic pie graph based on 3rd dropdown selection for category
# Add a callback to set the value of the catradio component to all options' values
@app.callback(
    Output('catradio', 'value'),
    Input('catradio', 'options'),
    Input('catradio', 'value'))
def select_all_options(options, values):
    if 'select-all' in values:
        return [x['value'] for x in options if x['value'] != 'select-all']
    else:
        return values

@app.callback(
    Output(component_id='piegraph_placing', component_property='figure'),
    Input(component_id='catradio', component_property='value'),
    Input(dropdown, component_property='value'),
    Input('event_sel', 'value')
)
def update_pie_graph(catradio_value, dropdown_value, event_sel_value):
    if not catradio_value or not dropdown_value:
        return {}

    if not event_sel_value:
        filtered_data = df.loc[(df['id'] == dropdown_value) & (df['category'].isin(catradio_value))]
    else:
        if isinstance(event_sel_value, str):
            event_sel_value = [event_sel_value]
        filtered_data = df.loc[(df['id'] == dropdown_value) & (df['category'].isin(catradio_value)) & (df['discipline'].isin(event_sel_value))]

    filtered_data1 = filtered_data.groupby(['place', 'category']).size().reset_index(name='number_of_placings')
    fig5 = px.pie(filtered_data1, values='number_of_placings', names='place', color='place',
                  color_discrete_sequence=px.colors.sequential.algae, color_discrete_map={'1.': 'gold', '2.': 'silver', '3.': 'saddlebrown'})
    fig5.update_layout(title="Placing by category selection(s)")
    return fig5

# Run app
if __name__ == '__main__':
    app.run_server(port=8053)
