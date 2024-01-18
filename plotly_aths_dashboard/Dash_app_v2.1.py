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

# Dropdown for athlete selection
dropdown = dcc.Dropdown(
    id='athlete-dropdown',
    options=[{'label': name, 'value': id} for id, name in zip(df['id'].unique(), df['name'].unique())],
    value=df['id'].unique()[0],
    clearable=False,
    searchable=True,
    style={'color': '#495057'} # Dark grey
)

# Dropdown for event selection
event_select = dcc.Dropdown(
    id='event-dropdown',
    options=[],
    multi=True,
    style={'color': '#495057'} # Dark grey
)

# Graph components
mygraph = dcc.Graph(id='mygraph')
sngraph = dcc.Graph(id='sngraph')
mapgraph = dcc.Graph(id='mapgraph')
placegraph = dcc.Graph(id='placegraph')
year_prog_graph = dcc.Graph(id='year_prog_graph')

# Layout
app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1('Australian Athletics Analytics', style={'textAlign': 'center', 'color': '#fff'}), width=12)]),
    dbc.Row([], style={'height': '20px'}), # row of nothing between the title and dropdowns
    dbc.Row([
        dbc.Col(dropdown, width=6, lg={'size': 3, 'offset': 3}),
        dbc.Col(event_select, width=6, lg={'size': 3})
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
    ])
], fluid=True)

# Callback to update event dropdown based on selected athlete
@app.callback(
    Output('event-dropdown', 'options'),
    Input('athlete-dropdown', 'value')
)
def update_event_dropdown(selected_athlete):
    athlete_events = df[df['id'] == selected_athlete]['discipline'].unique()
    return [{'label': event, 'value': event} for event in athlete_events]

# Callback for updating graphs
@app.callback(
    [Output('mygraph', 'figure'),
     Output('sngraph', 'figure'),
     Output('mapgraph', 'figure'),
     Output('placegraph', 'figure'),
     Output('year_prog_graph', 'figure')],
    [Input('athlete-dropdown', 'value'),
     Input('event-dropdown', 'value')]
)
def update_all_graphs(user_input, event_select1):
    # Filter data based on user input
    filtered_data = df[df['id'] == user_input]
    if event_select1:
        filtered_data = filtered_data[filtered_data['discipline'].isin(event_select1)]

    # Ensure the filtered data is not empty before plotting
    if filtered_data.empty:
        return [px.scatter(title="No Data Available")] * 5

    # Graph 1
    fig = px.scatter(filtered_data, x="date", y="resultscore",
                     color="disciplineCode", hover_data=["category", "place", "mark", "wind"])
    fig.update_layout(legend_title_text='', title="Event Results - Hover for more information!", title_x=0.4)

    # Graph 2
    dfb = filtered_data.copy()
    dfb['season'] = dfb['date'].dt.strftime('%Y')
    dfb['season'] = dfb['season'].astype(int)
    dfb['sn_best'] = dfb.groupby(['season', 'disciplineCode'])['resultscore'].transform('max')
    fig2 = px.line(dfb, x="season", y="sn_best", color="disciplineCode", markers=True)
    fig2.update_layout(legend_title_text='', title="Season's bests", title_x=0.4)

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
    fig3.update_traces(marker=dict(line=dict(width=2, color='Blue')), selector=dict(mode='markers'))
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
    # Add trend lines for each year
    for year in dfc['year'].unique():
        group = dfc[dfc['year'] == year]
        trendline_ols = px.scatter(group, x="date", y="resultscore", trendline="ols").data[1]
        trendline_ols['line']['color'] = 'red'  # Set color of trendline_ols to red
        trendline_lowess = px.scatter(group, x="date", y="resultscore", trendline="lowess").data[1]
        trendline_lowess['line']['color'] = 'blue'  # Set color of trendline_lowess to blue
        fig5.add_trace(trendline_ols)
        fig5.add_trace(trendline_lowess)

    return fig, fig2, fig3, fig4, fig5

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
