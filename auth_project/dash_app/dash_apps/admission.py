from dash import html, dcc, dash_table, _dash_renderer
from dash.dependencies import Input, Output
import dash_mantine_components as dmc
from django_plotly_dash import DjangoDash
import plotly.express as px
_dash_renderer._set_react_version("18.2.0")


app = DjangoDash('AdmissionsApp', external_stylesheets=dmc.styles.ALL)


from ..models import StudentData
all_students = StudentData.objects.all().order_by("year")


all_data = [
    {
        "Year": student.year,
        "Mech": student.mech,
        "Civil": student.civil,
        "EE": student.ee,
        "CSE": student.cse
    }
    for student in all_students
]


# # Layout for the Dash app
# app.layout = html.Div([
#     html.H1("Admissions Data Over Years", style={"textAlign": "center"}),

#     # Dropdown for year selection
#     html.Label("Select Year:"),
#     dcc.Dropdown(
#         id="year-dropdown",
#         options=[{"label": student.year, "value": student.year}
#                 for student in all_students],
#         placeholder="Select a year"
#     ),

#     dash_table.DataTable(
#         id="admissions-table",
#         data=all_data,
#         columns=[
#             {"name": "Year", "id": "Year"},
#             {"name": "Mech", "id": "Mech"},
#             {"name": "Civil", "id": "Civil"},
#             {"name": "EE", "id": "EE"},
#             {"name": "CSE", "id": "CSE"}
#         ],
#         page_size=3,  # Number of rows per page
#         style_table={'overflowX': 'auto'},  # Handle horizontal overflow
#         style_header={
#             'backgroundColor': 'rgb(230, 230, 230)',
#             'fontWeight': 'bold'
#         },
#         style_data={
#             'whiteSpace': 'normal',
#             'height': 'auto',
#         }
#     ),

#     html.A(
#         "Click here for more explantion",
#         href="http://127.0.0.1:8000/dash/graph_explained/",
#         style={"color": "blue", "textDecoration": "underline"}
#     ),

#     # Graph to display the data
#     dcc.Graph(id="admissions-graph")
# ])

# # Callback for updating the graph based on the selected year
# @app.callback(
#     Output("admissions-graph", "figure"),
#     [Input("year-dropdown", "value")]
# )
# def update_graph(selected_year):
#     if selected_year:
#         student = StudentData.objects.filter(year=selected_year).first()
#         if student:
#             branches = ["Mech", "Civil", "EE", "CSE"]
#             values = [student.mech, student.civil, student.ee, student.cse]

#             # Create bar chart
#             fig = px.bar(
#                 x=branches,
#                 y=values,
#                 labels={"x": "Branch", "y": "Number of Students"},
#                 title=f"Admissions for {selected_year}"
#             )
            
#             return fig


#     # Default graph
#     data = {
#         "Year": [],
#         "Branch": [],
#         "Admissions": []
#     }
#     for student in all_students:
#         for branch, value in zip(["Mech", "Civil", "EE", "CSE"], [student.mech, student.civil, student.ee, student.cse]):
#             data["Year"].append(student.year)
#             data["Branch"].append(branch)
#             data["Admissions"].append(value)

#     fig = px.bar(
#         data,
#         x="Year",
#         y="Admissions",
#         color="Branch",
#         barmode="group",
#         title="Admissions Over Years"
#     )
    
#     return fig





# Layout of the app
app.layout = html.Div(
    dmc.MantineProvider(
        withGlobalClasses=True,
        children=html.Div(
            children=[
                # Main Card
                dmc.Card(
                    children=[
                        # Title and Select Dropdown for Year
                        dmc.Title("Admissions Data Over Years", ta="center", order=1),
                        dmc.Text("Select Year:", size="sm", fw=500),
                        dmc.Select(
                            id="year-dropdown",
                            data=[{"label": student.year, "value": student.year} for student in all_students],
                            placeholder="Select a year",
                            searchable=True,
                            clearable=True
                        ),

                        dmc.Space(h=10),

                        # Table for displaying admission data
                        dmc.Table(
                            id="admissions-table",
                            striped=True,
                            highlightOnHover=True,
                            withTableBorder=True,
                            withColumnBorders=True,
                        ),
                        dmc.TableCaption("Students admission data as per the year"),

                        dmc.Space(h=10),

                        # Pagination control for table
                        dmc.Pagination(
                            id="table-pagination",
                            total=(len(all_data) + 2) // 3,  # Total pages (3 rows per page)
                            siblings=1,
                            boundaries=1,
                            value=1,  # Set the initial page to 1
                            style={"display": "flex", "justifyContent": "center", "textDecoration": "none"}
                        ),

                        # Link for further explanation
                        html.A(
                            dmc.Button(
                                "Click here for more explanation",
                                variant="gradient",
                                gradient={"from": "teal", "to": "lime", "deg": 105},
                            ),
                            href="http://127.0.0.1:8000/dash/graph_explained/",
                            target="_blank",  # Opens the link in a new tab,
                            style={"display": "flex", "justifyContent": "flex-end", "textDecoration": "none"}
                        ),

                        dmc.Space(h=20),

                        # Card containing the graph
                        dmc.Card(
                            dcc.Graph(id="admissions-graph"),
                            withBorder=True,
                            shadow="sm",
                            padding="lg"
                        )
                    ],
                    withBorder=True,
                    shadow="lg",
                    padding="xl"
                )
            ]
        )
    )
)

# Callback to update the table rows based on the selected page in pagination
@app.callback(
    Output("admissions-table", "children"),
    [Input("table-pagination", "value")]
)
def update_table(page_number):
    # Set how many rows to show per page
    rows_per_page = 3
    start = (page_number - 1) * rows_per_page
    end = start + rows_per_page

    # Slice data to show only the rows for the current page
    current_page_data = all_data[start:end]

    # Table header
    table_header = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Year"),
                dmc.TableTh("Mech"),
                dmc.TableTh("Civil"),
                dmc.TableTh("EE"),
                dmc.TableTh("CSE"),
            ]
        )
    )
    
    # Table body with rows for the current page
    table_body = dmc.TableTbody(
        [
            dmc.TableTr(
                [
                    dmc.TableTd(data["Year"]),
                    dmc.TableTd(data["Mech"]),
                    dmc.TableTd(data["Civil"]),
                    dmc.TableTd(data["EE"]),
                    dmc.TableTd(data["CSE"]),
                ]
            ) for data in current_page_data
        ]
    )

    return [table_header, table_body]

# Callback to update the admissions graph based on the selected year from the dropdown
@app.callback(
    Output("admissions-graph", "figure"),
    [Input("year-dropdown", "value")]
)
def update_graph(selected_year):
    if selected_year:
        # Filter the student data for the selected year
        student = StudentData.objects.filter(year=selected_year).first()
        if student:
            branches = ["Mech", "Civil", "EE", "CSE"]
            values = [student.mech, student.civil, student.ee, student.cse]

            fig = px.bar(
                x=branches,
                y=values,
                labels={"x": "Branch", "y": "Number of Students"},
                title=f"Admissions for {selected_year}"
            )
            return fig

    # Default graph (if no year is selected)
    data = {
        "Year": [],
        "Branch": [],
        "Admissions": []
    }
    for student in all_students:
        for branch, value in zip(["Mech", "Civil", "EE", "CSE"], [student.mech, student.civil, student.ee, student.cse]):
            data["Year"].append(student.year)
            data["Branch"].append(branch)
            data["Admissions"].append(value)

    fig = px.bar(
        data,
        x="Year",
        y="Admissions",
        color="Branch",
        barmode="group",
        title="Admissions Over Years"
    )
    return fig









"""Slider Graphs"""

# from dash import dcc, html, Input, Output
# import plotly.express as px
# from django_plotly_dash import DjangoDash

# # Create a DjangoDash app
# app = DjangoDash('AdmissionsApp')  # Unique name for the Dash app

# # Layout
# app.layout = html.Div([
#     html.H1("Dynamic Admissions Data Visualization", style={"textAlign": "center"}),

#     # Sliders for branches
#     html.Div([
#         html.Label("Mechanical:"),
#         dcc.Slider(
#             id='mech-slider',
#             min=0, max=500, step=1, value=100,
#             marks={i: str(i) for i in range(0, 501, 100)}
#         ),
#         html.Label("Civil:"),
#         dcc.Slider(
#             id='civil-slider',
#             min=0, max=500, step=1, value=100,
#             marks={i: str(i) for i in range(0, 501, 100)}
#         ),
#         html.Label("Electrical:"),
#         dcc.Slider(
#             id='ee-slider',
#             min=0, max=500, step=1, value=100,
#             marks={i: str(i) for i in range(0, 501, 100)}
#         ),
#         html.Label("Computer Science:"),
#         dcc.Slider(
#             id='cse-slider',
#             min=0, max=500, step=1, value=100,
#             marks={i: str(i) for i in range(0, 501, 100)}
#         ),
#     ], style={"marginBottom": "20px"}),

#     # Graphs
#     html.Div([
#         dcc.Graph(id='bar-chart'),
#         dcc.Graph(id='line-graph'),
#         dcc.Graph(id='pie-chart'),
#     ]),
# ])

# # Callback to update graphs
# @app.callback(
#     [Output('bar-chart', 'figure'),
#      Output('line-graph', 'figure'),
#      Output('pie-chart', 'figure')],
#     [Input('mech-slider', 'value'),
#      Input('civil-slider', 'value'),
#      Input('ee-slider', 'value'),
#      Input('cse-slider', 'value')]
# )
# def update_graphs(mech, civil, ee, cse):
#     # Data
#     branches = ["Mech", "Civil", "EE", "CSE"]
#     values = [mech, civil, ee, cse]

#     # Bar Chart
#     bar_chart = px.bar(
#         x=branches,
#         y=values,
#         labels={"x": "Branch", "y": "Number of Students"},
#         title="Bar Chart - Current Admissions"
#     )

#     # Line Graph
#     line_graph = px.line(
#         x=branches,
#         y=values,
#         labels={"x": "Branch", "y": "Number of Students"},
#         title="Line Graph - Current Admissions"
#     )

#     # Pie Chart
#     pie_chart = px.pie(
#         values=values,
#         names=branches,
#         title="Pie Chart - Admissions Distribution",
#         labels={"values": "Number of Students"}
#     )

#     return bar_chart, line_graph, pie_chart
