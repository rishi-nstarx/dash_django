from django_plotly_dash import DjangoDash
from dash import html, dcc,_dash_renderer
import dash_mantine_components as dmc
import plotly.express as px

from dash.dependencies import Input, Output
_dash_renderer._set_react_version("18.2.0")


# Define the Dash app
app = DjangoDash("AdmissionsAppExplained")




# from ..models import StudentData
# all_students = StudentData.objects.all().order_by("year")

# # Layout with multiple charts
# app.layout = html.Div([
#     # Title
#     html.H1(
#         "Admissions Data Dashboard",
#         style={"textAlign": "center", "marginBottom": "20px"}
#     ),
    
#     # Dropdown for selecting the year
#     html.Div([
#         html.Label("Select Year:"),
#         dcc.Dropdown(
#             id="year-select",
#             options=[
#                 {"label": student.year, "value": student.year}
#                 for student in all_students
#             ],
#             placeholder="Choose a year",
#             clearable=True,
#             style={"width": "50%"}
#         ),
#     ], style={"textAlign": "center", "marginBottom": "30px"}),

#     # Graph containers
#     html.Div([
#         html.Div([
#             dcc.Graph(id="bar-chart")
#         ], style={"width": "32%", "display": "inline-block"}),

#         html.Div([
#             dcc.Graph(id="line-graph")
#         ], style={"width": "32%", "display": "inline-block"}),

#         html.Div([
#             dcc.Graph(id="pie-chart")
#         ], style={"width": "32%", "display": "inline-block"}),
#     ], style={"textAlign": "center", "marginTop": "20px"})
# ])




# Components with DMC.
from ..models import StudentData
all_students = StudentData.objects.all().order_by("year")


# Layout with multiple charts
app.layout = dmc.MantineProvider(
    withGlobalClasses=True,
    children=html.Div([
        # Title
        dmc.Title(
            "Admissions Data Dashboard",
            ta="center",
            order=1,
            style={"marginBottom": "20px"}
        ),

        # Dropdown for selecting the year
        dmc.Group(
            children=[
                dmc.Text("Select Year:", size="sm", fw=500),
                dmc.Select(
                    id="year-select",
                    data=[
                        {"label": student.year, "value": student.year}
                        for student in all_students
                    ],
                    placeholder="Choose a year",
                    searchable=True,
                    clearable=True,
                    style={"width": "300px"}
                ),
            ],
            justify="center",
            style={"marginBottom": "30px"}
        ),

        # Graph containers
        dmc.Group(
            children=[
                dmc.Card(
                    dcc.Graph(id="bar-chart"),
                    withBorder=True,
                    shadow="sm",
                    padding="lg",
                    style={"width": "32%"}
                ),
                dmc.Card(
                    dcc.Graph(id="line-graph"),
                    withBorder=True,
                    shadow="sm",
                    padding="lg",
                    style={"width": "32%"}
                ),
                dmc.Card(
                    dcc.Graph(id="pie-chart"),
                    withBorder=True,
                    shadow="sm",
                    padding="lg",
                    style={"width": "32%"}
                ),
            ],
            justify="center",
            grow=True,
            style={"marginTop": "20px"}
        )
    ])
)





# Callback to update all graphs
@app.callback(
    [Output("bar-chart", "figure"),
     Output("line-graph", "figure"),
     Output("pie-chart", "figure")],
    [Input("year-select", "value")]
)
def update_graphs(selected_year):

    # Line graph preparation
    line_data = {
        "Year": [],
        "Branch": [],
        "Students": []
    }

    for student in all_students:
        line_data["Year"].extend([student.year] * 4)
        line_data["Branch"].extend(["Mech", "Civil", "EE", "CSE"])
        line_data["Students"].extend([student.mech, student.civil, student.ee, student.cse])

    # Line graph
    line_graph = px.line(
        x=line_data["Year"],
        y=line_data["Students"],
        color=line_data["Branch"],
        labels={"x": "Year", "y": "Number of Students"},
        title="Trend of Students Across Years"
    )

    if selected_year:
        student = StudentData.objects.filter(year=selected_year).first()
        if student:
            # Data for bar and pie charts
            branches = ["Mech", "Civil", "EE", "CSE"]
            values = [int(student.mech), int(student.civil), int(student.ee), int(student.cse)]

            # Bar Chart
            bar_chart = px.bar(
                x=branches,
                y=values,
                labels={"x": "Branch", "y": "Number of Students"},
                title=f"Bar Chart - Admissions for {selected_year}"
            )

            # Pie Chart
            pie_chart = px.pie(
                values=values,
                names=branches,
                title=f"Pie Chart - Admissions Distribution for {selected_year}",
                labels={"values": "Number of Students"}
            )

            return bar_chart, line_graph, pie_chart

    # Return empty bar and pie charts if no year is selected
    empty_chart = px.bar(title="Select a year to view data")
    return empty_chart, line_graph, empty_chart

