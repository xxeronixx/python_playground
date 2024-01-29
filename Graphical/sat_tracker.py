import datetime
import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output
from skyfield.api import load
import pandas as pd

# Load TLE data from Celestrak
tle_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(tle_url)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


# Update the satellite positions
def update_positions(current_time):
    t = load.timescale().utc(
        current_time.year, current_time.month, current_time.day,
        current_time.hour, current_time.minute, current_time.second
    )

    data = []
    for sat in satellites:
        geocentric = sat.at(t)
        subpoint = geocentric.subpoint()
        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees
        altitude = subpoint.elevation.km
        elevation = altitude * 1000 # Convert altitude from km to meters

        data.append({'Satellite': sat.name, 'Latitude': latitude, 'Longitude': longitude,
                     'Altitude': altitude, 'Elevation': elevation})

    df = pd.DataFrame(data)
    return df


# Update the graph with satellite positions
@app.callback(Output('live-update-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    current_time = datetime.datetime.utcnow()
    data = update_positions(current_time)

    scatter = dict(
        mode='markers',
        name='Satellite Positions',
        type='scattergeo',
        lat=data['Latitude'],
        lon=data['Longitude'],
        text=data['Satellite'],
        marker=dict(size=8, color='red', opacity=0.5),
    )

    layout = dict(
        title='Live Satellite Tracker',
        showlegend=False,
        geo=dict(
            resolution=50,
            showland=True,
            showlakes=True,
            landcolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            lakecolor='rgb(255, 255, 255)',
            projection=dict(type='orthographic', rotation=dict(lon=-143, lat=61, roll=0)),
            lonaxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            ),
            lataxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            )
        ),
        width=1910,
        height=1020,
    )

    return {'data': [scatter], 'layout': layout}


# Multiple components can update every time interval gets fired.
@app.callback(Output('live-update-text', 'children'), Input('interval-component', 'n_intervals'))
def update_metrics(n):
    current_time = datetime.datetime.utcnow()
    data = update_positions(current_time)

    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(data['Longitude'][0]), style=style),
        html.Span('Latitude: {0:.2f}'.format(data['Latitude'][0]), style=style),
        html.Span('Altitude: {0:.2f} km'.format(data['Altitude'][0]), style=style),
        html.Span('Elevation: {0:.2f} meters'.format(data['Elevation'][0]), style=style)
    ]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
