
import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Image Display Test"),
    html.Img(src='World_Athletics_logo.png', style={'maxWidth': '100%', 'height': 'auto'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
