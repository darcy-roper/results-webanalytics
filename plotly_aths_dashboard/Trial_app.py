# trial app

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# -- Import data (importing csv into pandas)
df = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Athlete Results/Kelsey-Lee Barber.csv")
top10 = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Event_Rankings_Top10.csv")
nass_athletes = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/List of Nass Athletes.csv")
champs_df = pd.read_csv("/Users/newmac/Desktop/Athlete dashboard/Championship_Results.csv") # this is all champs results

df["Season"] = df["Season"].astype(str) # converts int to a str so the data becomes discrete not continuous

#champs_filter = champs_df[(champs_df.EVENT == event_input) & (champs_df.CHAMPS == champs_input)]  # need to be inputs

nme_col = nass_athletes['Name']  # returns only the colum with all athlete names


# ------------------------------------------------------------------------------
# App layout using BOOTSTRAP

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Web Application - NASS Athlete Analytics", style={'text-align': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(nme_col, id="slct_athlete", multi=False)
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='output_container', children=[]), html.Br()
        ], width=12)
    ]),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id='Results_chart', figure={})
        ], width=12),

        dbc.Col([
            dcc.Input(id="year_input", type='number', inputMode='numeric', value=2022,
                      max=2022, min=2010, step=1, required=True)
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='PBSB_chart', figure={})
        ], width=8, style={'text-align': 'right'})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='competition_map', figure={})
        ], width=12)
    ])


])



# ------------------------------------------------------------------------------
# create top10 comparison using Plotly Graph Objects
# Create figure
fig2 = go.Figure()

event_filter = df.copy()
event_filter = event_filter[(event_filter.Name == slct_athlete)]
event_filtered = pd.unique(event_filter["Event"])
dff = top10.copy()
dff = dff[(dff.EVENT == "should be based off athlete name")]

dff2 = df.copy()
dff2 = dff2[(dff2.Name == slct_athlete) & (dff2.Season == year_input)]

# The entries for the NASS athlete
# ---------------------------------------------------------
# Add trace for athlete PB to highlight
filt_PB = dff2["PB"].max()
fig2.add_trace(go.Scatter(x=[slct_athlete], y=[filt_PB], mode='markers', marker_symbol='star-diamond-dot', marker_color='purple', marker_size=15,
                         showlegend=False, hovertemplate="%{x} %{y} <extra>PB</extra>")) # the 'extra' tags change the "trace" label on the marker
# Add trace for athlete SB to highlight
filt_SB = dff2["SB"].max()
fig2.add_trace(go.Scatter(x=[slct_athlete], y=[filt_SB], mode='markers', marker_symbol='star-diamond-dot', marker_color='orange', marker_size=13,
                         showlegend=False, hovertemplate="%{x} %{y} <extra>SB</extra>"))


# The entries from the CSV data as taken from World athletics
# ---------------------------------------------------------
fig2.add_trace(go.Scatter(x=dff['Name'], y=dff['PB'], name="PB", mode='markers', marker_size=18, marker_color="green",
                         text=dff['Rank'], hovertemplate="%{x} %{y} <br> Current World Rank = %{text}"))
fig2.add_trace(go.Scatter(x=dff['Name'], y=dff['SB'], name="SB", mode='markers', marker_size=15, marker_color="blue",
                         text=dff['Rank'], hovertemplate="%{x} %{y} <br> Current World Rank = %{text}"))


# Update the horizontal lines for average figures
# ---------------------------------------------------------
# Add horizontal line for averages
av_PBs = dff["PB"].mean().round(2)
av_SBs = dff["SB"].mean().round(2)
fig2.add_hline(y=av_PBs, annotation_text="Average PB", annotation_position="bottom right", line_color="green")
fig2.add_hline(y=av_SBs, annotation_text="Average SB", annotation_position="bottom right", line_color="blue")


# Add figure title
fig2.update_layout(
    title_text="World Top 10 (points) PBs/SBs - Compared to Athlete")

# Set x-axis titles
fig2.update_xaxes(title_text="Athlete Name")
fig2.update_yaxes(title_text="Result (m)")



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='competition_map', component_property='figure'),
     Output(component_id='PBSB_chart', component_property='figure'),
     Output(component_id='Results_chart', component_property='figure')],
    [Input(component_id='slct_athlete', component_property='value'),
     Input(component_id='year_input', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The athlete chosen was: {}".format(option_slctd)

    #dff = df.copy()
    #dff = dff[dff["Name"] == option_slctd]  # filters the copy  of the df to only show the input athlete name
    #dff = dff[dff["Season"] == season_slctd]  # somehow input a second filter to select seasons

    # Plotly Express
    fig = px.scatter_geo(df, locations="Ctry", color="Continent", projection="natural earth", size="Competition_Count", title="Global Competition Footprint")

    chart = px.bar(df, x="Date", y="Result", color="Season", title="Results History", hover_data=['Competition', 'Country'])

    # appends the y-axis to smaller range
    chart.update_yaxes(range=[min(df["Result"]-.10), max(df["Result"]+.10)])
    chart.update_yaxes(rangemode='normal')



    return container, fig, chart, fig2


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
