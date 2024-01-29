import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json


# Function to get site status based on "resourceState"
def get_site_status(resource_state):
    return "Online" if resource_state == "online" else "Offline"


# Function to generate indicator based on status
# Function to generate indicator based on status
def generate_status_indicator(entry):
    # Access the relevant information for status determination
    resource_state = entry.get("resourceState", "")

    # Access the site name (externalId)
    site_name = entry.get("place", {}).get("externalId", "")

    # Access the up address (hostNumber)
    host_number = entry.get("networkInterface", [{}])[0].get("ipv4Address", [{}])[0].get("hostNumber", "")

    # Determine site status and generate indicator
    status = get_site_status(resource_state)

    # Determine background color based on status
    color = "green" if status == "Online" else "red"

    # Generate HTML element with the new style and class for offline indicators
    indicator_html = html.Div(children=[
        html.Div(children=[
            html.Div(site_name, className="site-name"),
        ],
            id=f"{site_name}-indicator",
            className="status-indicator" if status == "Online" else "status-indicator-offline",
        ),
        html.A(children=[html.Div(host_number, className="host-number")
                         ],
               style={'display': 'inline-block'},
               href=f"http://{host_number}",
               )],
        style={'display': 'flex', 'align-items': 'center', 'fontFamily': 'HelveticaNeue'})

    return indicator_html


# Sample function to read JSON from a file (replace with your actual file path)
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Define app layout
app.layout = html.Div(children=[
    html.H1("Site Status Indicators"),

    # Generate status indicators dynamically based on the JSON response
    html.Div(id='status-indicators'),
    dcc.Interval(
        id='interval-component',
        interval=5 * 60 * 1000,  # in milliseconds (5 minutes)
        n_intervals=0
    ),
])


# Callback to update the status indicators at regular intervals
@app.callback(
    Output('status-indicators', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_status_indicators(n_intervals):
    try:
        # Replace 'your_json_file.json' with your actual file path
        file_path = 'api_response.json'

        # Read JSON data from the file
        json_data = read_json_from_file(file_path)

        # Iterate over the inner lists and dictionaries
        status_indicators = []
        for inner_list in json_data:
            for entry in inner_list:
                # Generate status indicator for each entry
                indicator_html = generate_status_indicator(entry)
                status_indicators.append(indicator_html)

        return status_indicators

    except Exception as e:
        print(f"Error reading or processing JSON from file: {e}")
        raise PreventUpdate  # Prevent update if there's an error


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
