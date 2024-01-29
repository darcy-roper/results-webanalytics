#Dahsboard for single athlete views of their results history

import plotly.io as pio
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# Load WC 2022 data for B&W plots
wc_data = pd.read_csv('Datasets/WC22_Results.csv', sep=',')

# Customize Plotly template
plotly_template = pio.templates["plotly"]
plotly_template.layout = {
    'font': {'family': "Arial, sans-serif", 'color': '#fff', 'size': 14},
    'title': {'x': 0.5, 'xanchor': 'left'},
    'paper_bgcolor': '#262626',  # Light grey
    'plot_bgcolor': '#262626',   # Transparent background for plot
    'colorway': ['#BE95FE', '#FE863D', '#A5FA63', '#FF33F6'],  # Custom color scheme
}

# Initialize the Dash app with the custom template
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
pio.templates.default = plotly_template


default_athlete_id = 14336705
default_athlete_events = df[df['id'] == default_athlete_id]['discipline'].unique()

# Extract unique disciplines for the default athlete
default_athlete_disciplines = df[df['id'] == default_athlete_id]['discipline'].unique()
# Determine the default event
if 'Javelin Throw' in default_athlete_disciplines:
    default_event = 'Javelin Throw'
elif len(default_athlete_disciplines) > 0:
    # If 'Javelin Throw' is not available but there are other disciplines
    default_event = default_athlete_disciplines[0]
else:
    # If the default athlete has no disciplines listed
    default_event = None

# Dropdown for athlete selection
athlete_dropdown = dcc.Dropdown(
    id='athlete-dropdown',
    options=[{'label': name, 'value': id} for id, name in zip(df['id'].unique(), df['name'].unique())],
    value=default_athlete_id,
    clearable=False,
    searchable=True,
    style={'color': '#495057'}
)

# Dropdown for event selection
event_dropdown = dcc.Dropdown(
    id='event-dropdown',
    options=[{'label': event, 'value': event} for event in default_athlete_events],
    value=default_event,
    multi=True,
    style={'color': '#495057'}
)

# Graph components
mygraph = dcc.Graph(id='mygraph')
sngraph = dcc.Graph(id='sngraph')
mapgraph = dcc.Graph(id='mapgraph')
placegraph = dcc.Graph(id='placegraph')
year_prog_graph = dcc.Graph(id='year_prog_graph')
champ_bw_plot = dcc.Graph(id='champ_bw_plot')

# Layout
app.layout = dbc.Container([
    # Single row with the title, image, and "Powered by" text
    dbc.Row([
        # Column for the image
        dbc.Col(html.Img(src='/assets/World_Athletics_logo.png', style={'maxHeight': '65px', 'paddingLeft': '25px'}),
                width={'size': 2, 'offset': 0},
                class_name='top_rows',
                style={'display': 'flex', 'alignItems': 'flex-end'}),

        # Column for the "Powered by" text
        dbc.Col(html.Div('Powered by', style={'paddingLeft': '0px', 'alignSelf': 'flex-end', 'fontSize': '10px'}),
                width={'size': 1, 'offset': 0},
                class_name='top_rows',
                style={'display': 'flex', 'alignItems': 'flex-end'}),

        # Column for the title
        dbc.Col(html.H1('Australian Athlete Analytics',
                        style={'textAlign': 'center',
                               'color': '#262626',
                               'display': 'flex',
                               'alignItems': 'center',
                               'justifyContent': 'center',
                               'height': '100%'}),
                width={'size': 6, 'offset': 0},
                class_name='top_rows'),
        ], style={'height': '80px'}, class_name='top_rows'),

    dbc.Row([], style={'height': '15px'}), # another empty row

    # Row with dropdown elements
    dbc.Row([
        dbc.Col(athlete_dropdown, width=6, lg={'size': 3, 'offset': 3}),
        dbc.Col(event_dropdown, width=6, lg={'size': 3})
    ]),
    dbc.Row([], style={'height': '20px'}),

    # Rows for each graphs
    dbc.Row([
        dbc.Col(id='mygraph-wrapper', children=[dcc.Graph(id='mygraph')], width=12, lg=6),
        dbc.Col(id='sngraph-wrapper', children=[dcc.Graph(id='sngraph')], width=12, lg=6)
    ]),
    dbc.Row([
        dbc.Col(id='mapgraph-wrapper', children=[dcc.Graph(id='mapgraph')], width=12, lg=6),
        dbc.Col(id='placegraph-wrapper', children=[dcc.Graph(id='placegraph')], width=12, lg=6)
    ]),
    dbc.Row([
        dbc.Col(id='year_prog_graph-wrapper', children=[dcc.Graph(id='year_prog_graph')], width=12)
    ]),
    dbc.Row([
        dbc.Col(id='champ_bw_plot-wrapper', children=[dcc.Graph(id='champ_bw_plot')], width=8),
    ]),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0), # 1 second
    dcc.Store(id='initialization-store', data={'is_initialized': False}),
], fluid=True)

# Callback to update event dropdown based on selected athlete and default to most frequent event
@app.callback(
    [Output('event-dropdown', 'options'),
     Output('event-dropdown', 'value')],
    Input('athlete-dropdown', 'value'))
def update_event_dropdown(selected_athlete):
    athlete_events = df[df['id'] == selected_athlete]['discipline'].value_counts()
    # Determine the most frequent event
    most_frequent_event = athlete_events.idxmax() if not athlete_events.empty else None
    # Prepare options for the event dropdown
    options = [{'label': event, 'value': event} for event in athlete_events.index]
    return options, most_frequent_event

# New callback to set initialization state
@app.callback(
    Output('initialization-store', 'data'),
    Input('athlete-dropdown', 'value'),
    Input('event-dropdown', 'value'))
def set_initialization_state(athlete_value, event_value):
    if athlete_value == default_athlete_id and (event_value == default_event or event_value == [default_event]):
        return {'is_initialized': True}
    return dash.no_update


# graph 1 callback
@app.callback(
    Output('mygraph-wrapper', 'children'),  # Target the wrapper's 'children' property
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')],
    [State('event-dropdown', 'value')])
def update_mygraph(athlete_id, event_trigger, event_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # Determine which event value to use
    events = event_trigger if triggered_id == 'event-dropdown' else event_state

    # Further filter the data if events are selected
    if events:
        if isinstance(events, list):
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Function to return figure
    fig1 = create_figure1(filtered_data)

    # If the callback was triggered by the athlete dropdown, wrap in dcc.Loading
    if triggered_id == 'athlete-dropdown':
        return dcc.Loading(children=dcc.Graph(figure=fig1), type="default")
    else:
        # If triggered by the event dropdown, return the graph only
        return dcc.Graph(figure=fig1)


# functions to create each figure
def create_figure1(filtered_data):
    # Create the figure for 'mygraph'
    fig1 = px.scatter(filtered_data, x="date", y="resultscore",
                      color="disciplineCode", hover_data=["category", "place", "mark", "wind"],
                      size_max=8)
    fig1.update_layout(
        legend_title_text='',
        title="Event Results",
        title_x=0.4)
    # Update x-axis and y-axis labels
    fig1.update_xaxes(title='')  # remove x-axis label
    fig1.update_yaxes(title='Result Score')  # rename y-axis label
    fig1.update_traces(marker=dict(size=10, line=dict(width=1, color='Black')))

    return fig1


# Graph 2 callback
@app.callback(
    Output('sngraph-wrapper', 'children'),
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')],
    [State('event-dropdown', 'value')])
def update_sngraph(athlete_id, event_trigger, event_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # Determine which event value to use
    events = event_trigger if triggered_id == 'event-dropdown' else event_state

    # Further filter the data if events are selected
    if events:
        if isinstance(events, list):
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Create the figure for 'sngraph'
    fig2 = create_figure2(filtered_data)

    # Wrap the figure in loading component if triggered by athlete-dropdown
    if triggered_id == 'athlete-dropdown':
        return dcc.Loading(children=dcc.Graph(figure=fig2))
    else:
        return dcc.Graph(figure=fig2)


# Function to create figure for Graph 2
def create_figure2(filtered_data):
    dfb = filtered_data.copy()
    dfb['season'] = dfb['date'].dt.strftime('%Y')
    dfb['season'] = dfb['season'].astype(int)
    dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')
    fig2 = px.line(dfb, x="season", y="sn_best", color="disciplineCode", markers=True)
    fig2.update_layout(legend_title_text='', title="Season's bests", title_x=0.4)
    fig2.update_xaxes(title='') # remove xaxis title
    fig2.update_traces(line=dict(width=3), marker=dict(size=10, line=dict(width=1, color='Black')))
    return fig2


# graph 3 callback
@app.callback(
    Output('mapgraph-wrapper', 'children'),
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')],
    [State('event-dropdown', 'value')])
def update_mapgraph(athlete_id, event_trigger, event_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # Determine which event value to use
    events = event_trigger if triggered_id == 'event-dropdown' else event_state

    # Further filter the data if events are selected
    if events:
        if isinstance(events, list):
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Create the figure for 'mapgraph'
    fig3 = create_figure3(filtered_data)

    # Wrap the figure in loading component if triggered by athlete-dropdown
    if triggered_id == 'athlete-dropdown':
        return dcc.Loading(children=dcc.Graph(figure=fig3))
    else:
        return dcc.Graph(figure=fig3)

# Graph 3 - update map
def create_figure3(filtered_data):
    dff = filtered_data.copy()
    dff['count'] = dff.groupby(['country'])['__typename'].transform('count')
    fig3 = px.scatter_geo(dff, locations="country", color="country",
                          size='count', projection="orthographic")
    fig3.update_layout(
        title='Travel Footprint',
        title_x=0.4,
        geo=dict(
            bgcolor='#262626',  # Set background color of the geo (map) area
            showland=True, landcolor="#A5FA63",  # Optionally set the land color if needed
            showocean=True, oceancolor="#0E4F77"  # Optionally set the ocean color if needed
        )
    )
    fig3.update_traces(marker=dict(line=dict(width=1, color='Black')), selector=dict(mode='markers'))
    fig3.update_traces(marker_sizemin=5, selector=dict(mode='markers'))
    return fig3


# graph 4 callback
@app.callback(
    Output('placegraph-wrapper', 'children'),
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')],
    [State('event-dropdown', 'value')])
def update_placegraph(athlete_id, event_trigger, event_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # Determine which event value to use
    events = event_trigger if triggered_id == 'event-dropdown' else event_state

    # Further filter the data if events are selected
    if events:
        if isinstance(events, list):
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Create the figure for 'placegraph'
    fig4 = create_figure4(filtered_data)

    # Wrap the figure in loading component if triggered by athlete-dropdown
    if triggered_id == 'athlete-dropdown':
        return dcc.Loading(children=dcc.Graph(figure=fig4))
    else:
        return dcc.Graph(figure=fig4)

# Graph 4 - Placing
def create_figure4(filtered_data):
    dfa = filtered_data.copy()
    hovertemp1 = "<b>Category: </b> %{label} <br>"
    hovertemp1 += "<b>Number of appearances: </b> %{value}"
    dfa1 = dfa.groupby(['place', 'category']).size().reset_index(name='number_of_placings')  # apply grouping to count number of comp appearances
    fig4 = px.pie(dfa1, values='number_of_placings', names='category', color='category',
                  color_discrete_map={'A': 'gold', 'B': 'silver', 'C': 'saddlebrown'})
    fig4.update_layout(title='Competition appearances by meet category', title_x=0.3)
    fig4.update_traces(hovertemplate=hovertemp1)
    return fig4

# graph 5 callback
@app.callback(
    Output('year_prog_graph-wrapper', 'children'),
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')],
    [State('event-dropdown', 'value')])
def update_year_prog_graph(athlete_id, event_trigger, event_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # Determine which event value to use
    events = event_trigger if triggered_id == 'event-dropdown' else event_state

    # Further filter the data if events are selected
    if events:
        if isinstance(events, list):
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Create the figure for 'year_prog_graph'
    fig5 = create_figure5(filtered_data)

    # Wrap the figure in loading component if triggered by athlete-dropdown
    if triggered_id == 'athlete-dropdown':
        return dcc.Loading(children=dcc.Graph(figure=fig5))
    else:
        return dcc.Graph(figure=fig5)


# Graph 5 - trends in each year
def create_figure5(filtered_data):
    dfc = filtered_data.copy()
    dfc['year'] = dfc['date'].dt.strftime('%Y')
    dfc['year'] = dfc['year'].astype(int)
    fig5 = px.scatter(dfc, x="date", y="resultscore",
                  color="discipline", hover_data=["category", "place", "mark", "wind"])
    fig5.update_layout(legend_title_text='', title="Season rates of progression", title_x=0.45)
    fig5.update_traces(marker=dict(size=10, line=dict(width=1, color='Black'))) # increase marker size
    fig5.update_yaxes(title="Result Score")
    fig5.update_xaxes(title="")
    # Add trend lines for each year
    for year in dfc['year'].unique():
        group = dfc[dfc['year'] == year]
        trendline_ols = px.scatter(group, x="date", y="resultscore", trendline="ols").data[1]
        trendline_ols['line']['color'] = 'Orange'  # Set color of trendline_ols to red
        trendline_lowess = px.scatter(group, x="date", y="resultscore", trendline="lowess").data[1]
        trendline_lowess['line']['color'] = 'White'  # Set color of trendline_lowess to blue
        fig5.add_trace(trendline_ols)
        fig5.add_trace(trendline_lowess)
    return fig5


####attempt to create 6th graph (box plot)######
# Callback for Graph 6 (Box plot based on discipline and indirectly determined athlete's sex)
@app.callback(
    Output('champ_bw_plot-wrapper', 'children'),
    [Input('athlete-dropdown', 'value'),  # This provides the name of the athlete
     Input('event-dropdown', 'value')])   # This provides the discipline
def update_box22(athlete_name, discipline):
    # Extract the sex of the selected athlete from the DataFrame
    athlete_sex = df[df['id'] == athlete_name]['sex'].iloc[0]

    # Filter wc_data for WC_2022
    filtered_data_2022 = wc_data[(wc_data['discipline'] == discipline) &
                                 (wc_data['sex'] == athlete_sex) &
                                 (wc_data['champs'] == 'WC_2022')]

    # Filter wc_data for WC_2023
    filtered_data_2023 = wc_data[(wc_data['discipline'] == discipline) &
                                 (wc_data['sex'] == athlete_sex) &
                                 (wc_data['champs'] == 'WC_2023')]

    # Create the figure for 'box and whisker' for both years
    fig6 = create_boxplot(filtered_data_2022, filtered_data_2023, discipline, athlete_sex)

    # Return the figure wrapped in dcc.Graph
    return dcc.Graph(figure=fig6)

# Function to create a box plot for both WC_2022 and WC_2023
def create_boxplot(data_2022, data_2023, discipline, sex):
    fig6 = go.Figure()

    # Check if filtered data for 2022 is not empty and add box plot
    if not data_2022.empty:
        fig6.add_trace(go.Box(y=data_2022['resultscore'], name='Oregon 2022'))

    # Check if filtered data for 2023 is not empty and add box plot
    if not data_2023.empty:
        fig6.add_trace(go.Box(y=data_2023['resultscore'], name='Budapest 2023'))

    # Update the layout and titles
    fig6.update_layout(
        title=f'{discipline} ({sex}) - Major Championship Final',
        yaxis_title='Result Score')

    return fig6


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
