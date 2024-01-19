#Dahsboard for single athlete views of their results history

import plotly.io as pio
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

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

# Layout
app.layout = dbc.Container([
    # Single row with the title, image, and "Powered by" text
    dbc.Row([
        # Column for the image
        dbc.Col(html.Img(src='assets/World_Athletics_logo.png', style={'maxHeight': '50px', 'maxWidth': '100px', 'paddingLeft': '50px'}),
                width={'size': 1, 'offset': 0},
                class_name='top_rows',
                style={'display': 'flex', 'alignItems': 'center'}),

        # Column for the "Powered by" text
        dbc.Col(html.Div('Powered by', style={'paddingLeft': '10px', 'alignSelf': 'center'}),
                width={'size': 3, 'offset': 0},
                class_name='top_rows',
                style={'display': 'flex', 'alignItems': 'center'}),

        # Column for the title
        dbc.Col(html.H1('Australian Athlete Analytics',
                        style={'textAlign': 'center',
                               'color': '#262626',
                               'display': 'flex',
                               'alignItems': 'center',
                               'justifyContent': 'center',
                               'height': '100%'}),
                width={'size': 8, 'offset': 0},
                class_name='top_rows'),
        ], style={'height': '80px'}, class_name='top_rows'),

    dbc.Row([], style={'height': '15px'}), # another empty row

    # Row with dropdown elements
    dbc.Row([
        dbc.Col(athlete_dropdown, width=6, lg={'size': 3, 'offset': 3}),
        dbc.Col(event_dropdown, width=6, lg={'size': 3})
    ]),
    dbc.Row([], style={'height': '20px'}),
    dbc.Row([
        dbc.Col(mygraph, width=12, lg=6),
        dbc.Col(sngraph, width=12, lg=6)
    ]),
    dbc.Row([
        dbc.Col(mapgraph, width=12, lg=6),
        dbc.Col(placegraph, width=12, lg=6)
    ]),
    dbc.Row([
        dbc.Col(year_prog_graph, width=12)
    ]),
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),# 1 second
    dcc.Store(id='initialization-store', data={'is_initialized': False}),
], fluid=True)

# Callback to update event dropdown based on selected athlete and default to most frequent event
@app.callback(
    [Output('event-dropdown', 'options'),
     Output('event-dropdown', 'value')],
    Input('athlete-dropdown', 'value'))
def update_event_dropdown(selected_athlete):
    # Get the disciplines for the selected athlete
    athlete_disciplines = df[df['id'] == selected_athlete]['discipline']

    # Count the occurrences of each discipline and find the most frequent one
    most_frequent_discipline = athlete_disciplines.value_counts().idxmax()

    # Prepare the options for the event dropdown
    options = [{'label': event, 'value': event} for event in athlete_disciplines.unique()]

    return options, most_frequent_discipline

# New callback to set initialization state
@app.callback(
    Output('initialization-store', 'data'),
    Input('athlete-dropdown', 'value'),
    Input('event-dropdown', 'value'))
def set_initialization_state(athlete_value, event_value):
    if athlete_value == default_athlete_id and (event_value == default_event or event_value == [default_event]):
        return {'is_initialized': True}
    return dash.no_update

# Callback for updating graphs
@app.callback(
    [Output('mygraph', 'figure'),
     Output('sngraph', 'figure'),
     Output('mapgraph', 'figure'),
     Output('placegraph', 'figure'),
     Output('year_prog_graph', 'figure')],
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')])
def update_graphs(athlete_id, events):
    # Filter data for the selected athlete
    filtered_data = df[df['id'] == athlete_id]

    # If any events are selected, further filter the data
    if events:
        if isinstance(events, list):
            # If multiple events are selected
            filtered_data = filtered_data[filtered_data['discipline'].isin(events)]
        else:
            # If only one event is selected
            filtered_data = filtered_data[filtered_data['discipline'] == events]

    # Check if data is available for plotting
    if filtered_data.empty:
        return [px.scatter(title="No Data Available")] * 5

    # Graph 1
    fig = px.scatter(filtered_data, x="date", y="resultscore",
                     color="disciplineCode", hover_data=["category", "place", "mark", "wind"],
                     size_max=8)  # to increase max marker size
    fig.update_layout(
        legend_title_text='',
        title="Event Results - Hover for more information!",
        title_x=0.4)
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='Black')))  # increase marker size and border width

    # Graph 2
    dfb = filtered_data.copy()
    dfb['season'] = dfb['date'].dt.strftime('%Y')
    dfb['season'] = dfb['season'].astype(int)
    dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')
    fig2 = px.line(dfb, x="season", y="sn_best", color="disciplineCode", markers=True)
    fig2.update_layout(legend_title_text='', title="Season's bests", title_x=0.4)
    fig2.update_traces(line=dict(width=3), marker=dict(size=10, line=dict(width=1, color='Black')))
    # line above increase line and marker size and border width

    # Graph 3 - update map
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


    # Graph 4 - Placing
    dfa = filtered_data.copy()
    hovertemp1 = "<b>Category: </b> %{label} <br>"
    hovertemp1 += "<b>Number of appearances: </b> %{value}"
    dfa1 = dfa.groupby(['place', 'category']).size().reset_index(name='number_of_placings')  # apply grouping to count number of comp appearances
    fig4 = px.pie(dfa1, values='number_of_placings', names='category', color='category',
                  color_discrete_map={'A': 'gold', 'B': 'silver', 'C': 'saddlebrown'})
    fig4.update_layout(title='Competition appearances by meet category', title_x=0.3)
    fig4.update_traces(hovertemplate=hovertemp1)


    # Graph 5 - trends in each year
    dfc = filtered_data.copy()
    dfc['year'] = dfc['date'].dt.strftime('%Y')
    dfc['year'] = dfc['year'].astype(int)
    fig5 = px.scatter(dfc, x="date", y="resultscore",
                  color="discipline", hover_data=["category", "place", "mark", "wind"])
    fig5.update_layout(legend_title_text='', title="Season rates of progression", title_x=0.45)
    fig5.update_traces(marker=dict(size=10, line=dict(width=1, color='Black'))) # increase marker size
    # Add trend lines for each year
    for year in dfc['year'].unique():
        group = dfc[dfc['year'] == year]
        trendline_ols = px.scatter(group, x="date", y="resultscore", trendline="ols").data[1]
        trendline_ols['line']['color'] = 'Orange'  # Set color of trendline_ols to red
        trendline_lowess = px.scatter(group, x="date", y="resultscore", trendline="lowess").data[1]
        trendline_lowess['line']['color'] = 'White'  # Set color of trendline_lowess to blue
        fig5.add_trace(trendline_ols)
        fig5.add_trace(trendline_lowess)

    return fig, fig2, fig3, fig4, fig5

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
