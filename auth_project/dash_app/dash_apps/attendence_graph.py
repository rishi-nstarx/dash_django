from django_plotly_dash import DjangoDash
from dash import html,dcc, callback_context
from dash.dependencies import Input, Output
import plotly.express as px
from django_plotly_dash.util import store_initial_arguments, get_initial_arguments

from django.core.cache import cache

# from dash_app.utils import get_current_cache_id


# import logging

# # Configure logger to capture logs (this is optional if logs are already configured)
# logger = logging.getLogger('dash_app_logs')

import json


app = DjangoDash("AttendenceReport")


# Layout
app.layout = html.Div([

    html.H1(
        "Attendance Report",
        style={"textAlign": "center", "marginBottom": "20px"}
    ),

    # Dropdown for year selection
    html.Label("Want to reload data:"),
    dcc.Dropdown(
        id="option-dropdown",
        options=[{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
        placeholder="Select an option"
    ),

    html.Div([
        html.Div([
            dcc.Graph(id="bar-chart")
        ], style={"width": "50%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="line-graph")
        ], style={"width": "50%", "display": "inline-block"}),
    ], style={"textAlign": "center", "marginTop": "20px"})
])

# Callback
@app.callback(
    [Output("bar-chart", "figure"),
     Output("line-graph", "figure")],
    [Input("option-dropdown", "value")]
)
def update_graph(selected_options):

    # Extract cache ID from logs
    # cache_id = extract_cache_id_from_logs('path_to_your_django_log_file')
    # cache_id = get_current_cache_id()

    # Access the current user from initial arguments
    # initial_args = callback_context.triggered
    # initial_arguments = get_initial_arguments(None, cache_id)
    # user_id = initial_arguments.get("user_id")


    if 1 == selected_options:

        def fetch_data():
            from ..models import AttendenceData # Relative import prevents from error.
            attendence_data = AttendenceData.objects.filter(student_id=5)
            return attendence_data
        
        # Month ordering
        MONTH_ORDER = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7,
        'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }
    
        attendence_data = fetch_data()
        sorted_attendence_data = sorted(attendence_data, key=lambda record: MONTH_ORDER[record.month])

        line_data = {
            "Months": [],
            "Days": []
        }

        for attendenec in sorted_attendence_data:
            line_data["Months"].append(attendenec.month)
            line_data["Days"].append(attendenec.days_in_month)

        line_graph = px.line(
            x=line_data["Months"],
            y=line_data["Days"],
            labels={"x": "Months", "y": "Total Days"},
            title= f"History of Student's per month attendence"
        )

        bar_chart = px.bar(
            x=line_data["Months"],
            y=line_data["Days"],
            labels={"x": "Months", "y": "Total Days"},
            title= f"Bar Graph representation of Student's per month attendence"
        )

        return bar_chart, line_graph
    return {}, {}





# # Define your Dash app layout
# app.layout = html.Div([
#     html.H1("Hello, World!", style={"textAlign": "center"})
# ])

# # Use get_current_user later in callbacks/views
# def fetch_user_data():
#     from dash_app.utils import get_current_user
#     user = get_current_user()  # Lazy import avoids initialization conflict
#     return user




# import re
# import logging

# def extract_cache_id_from_logs(log_file_path):
    
#     cache_id_pattern = r'dpd-initial-args-([a-f0-9]{32})'
    
#     # Read the log file and search for cache_id pattern
#     with open(log_file_path, 'r') as log_file:
#         logs = log_file.read()
        
#     cache_ids = re.findall(cache_id_pattern, logs)
    
#     if cache_ids:
#         return cache_ids[0]  # Return the first cache_id found
#     else:
#         return None  # No cache_id found
