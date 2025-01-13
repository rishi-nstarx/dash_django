from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from websocket import create_connection
import threading
import json
import time

# Initialize Dash app
app = DjangoDash("LiveApp")
app.title = "Real-Time Line Graph Dashboard"

# WebSocket Configuration
WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/live-data/"
live_data = {"Zone A": [], "Zone B": [], "Zone C": [], "Zone D": []}
timestamps = []  # Store timestamps for x-axis

# Function to fetch data from WebSocket
def fetch_live_data():
    ws = create_connection(WEBSOCKET_URL)
    while True:
        try:
            response = json.loads(ws.recv())
            timestamp = time.strftime('%H:%M:%S', time.gmtime())
            timestamps.append(timestamp)
            if len(timestamps) > 50:  # Limit to 50 points
                timestamps.pop(0)

            for zone, value in response.items():
                live_data[zone].append(value)
                if len(live_data[zone]) > 50:  # Limit history to 50 points
                    live_data[zone].pop(0)
        except Exception as e:
            print("WebSocket error:", e)
            break

thread = threading.Thread(target=fetch_live_data, daemon=True)

thread_status = False
def wait():
    time.sleep(3)
    thread.start()
    global thread_status
    thread_status = True


# App Layout
app.layout = html.Div([
    html.H1("Real-Time Line Graph Dashboard", 
            style={"textAlign": "center"}),

    dcc.Graph(id="line-graph"),  # Graph for real-time line chart

    dcc.Interval(id="update-interval", 
                 interval=1000, 
                 n_intervals=0),  # Refresh every 1 second
])

# Callback to update the graph
@app.callback(
    Output("line-graph", "figure"),
    Input("update-interval", "n_intervals")
)
def update_graph(n_intervals):
    # Ensure data is available before creating the figure
    if timestamps:
        fig = go.Figure()
        for zone, values in live_data.items():
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=values,
                mode="lines+markers",
                name=zone
            ))

        fig.update_layout(
            title="Live Zone Data Progression",
            xaxis_title="Time",
            yaxis_title="Values",
            template="plotly_dark",
            xaxis=dict(showline=True, showgrid=True),
            yaxis=dict(showline=True, showgrid=True),
        )
        return fig
    else:
        # Placeholder figure when no data is available
        return go.Figure().update_layout(title="Waiting for data...")