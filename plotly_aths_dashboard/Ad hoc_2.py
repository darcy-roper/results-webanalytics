
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time

# Load data
df = pd.read_csv('Dataframe_Analysis.csv', sep='|')
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)


# Initialize the Dash app
app = dash.Dash(__name__)

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

mygraph = dcc.Graph(id='mygraph')

# App layout
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
        dbc.Col(id='mygraph-wrapper', children=[dcc.Graph(id='mygraph')], width=12, lg=6)
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
        title="Event Results - Hover for more information!",
        title_x=0.4)
    # Update x-axis and y-axis labels
    fig1.update_xaxes(title='')  # remove x-axis label
    fig1.update_yaxes(title='Result Score')  # rename y-axis label
    fig1.update_traces(marker=dict(size=10, line=dict(width=1, color='Black')))

    return fig1

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
