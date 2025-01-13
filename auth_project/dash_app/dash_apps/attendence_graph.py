from django_plotly_dash import DjangoDash
from dash import html,dcc, _dash_renderer
from dash.dependencies import Input, Output
import plotly.express as px


_dash_renderer._set_react_version("18.2.0")

app = DjangoDash("AttendenceReport")
def fetch_data(id):
    from ..models import AttendenceData # Relative import prevents from error.
    global attendence_data
    attendence_data = AttendenceData.objects.filter(student_id=id)

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

    if 1 == selected_options:
        
        # Month ordering
        MONTH_ORDER = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7,
        'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }
    
        # attendence_data = fetch_data()
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
