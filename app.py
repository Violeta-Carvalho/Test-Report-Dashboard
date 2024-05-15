from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import os
from utils import plotly_dual_axis, get_all_dates
from manipulation import get_vus_df, get_http_requests_df, get_page_performance_df, get_vus_session_length, get_load_summary

app = Dash(__name__)
app._favicon = "favico.ico"
app.title = "Test Report Traive"
app.css.config.serve_locally = True

dates = get_all_dates()

page_performance_df = get_page_performance_df(dates[0])
urls = page_performance_df["URL"].unique().tolist()
urls.append("All")

app.layout = html.Div([
    html.Div(className="header", children=[
        html.H1(f"Test Performed on {dates[0]}", id="title"),
        html.Div(className="flex-center", children=[
            html.P("Select a new test:"),
            dcc.Dropdown(id='date', options=dates, value=dates[0], className="input", clearable=False), 
        ]),
    ]),
    html.Div(className="flex-center", children=[
        html.Div(children=[dcc.Graph(id='vus', className="half-graph")]),
        html.Div(children=[dcc.Graph(id='http-requests', className="half-graph")]),
    ]),
    
    html.Div(className="flex-center", children=[
        html.P("Select URL for Page Performance:"),
        dcc.Dropdown(id='url', options=urls, value="All", className="input"),  
    ]),
    dcc.Graph(id="page-performance", className="graph"),
    
    dcc.Graph(id='load-summary', className="graph"),
    dcc.Graph(id='vus-session-length', className="graph"),
])

@app.callback(
    Output("title", "children"),
    Input("date", "value"))
def url_options(date):
    date = date.replace("-", "/").replace("T", ", ")
    return f"Test Performed on {date}" 

@app.callback(
    Output("url", "options"),
    Input("date", "value"))
def url_options(date):
    page_performance_df = get_page_performance_df(date)
    new_urls = page_performance_df["URL"].unique().tolist()
    new_urls.append("All")
    return new_urls  

@app.callback(
    Output("http-requests", "figure"),
    Input("date", "value")) 
def generate_chart(date):
    http_requests_df = get_http_requests_df(date)
    http_requests_fig = px.pie(http_requests_df, title="HTTP Request Codes", values="Amount of Requests", names="Response Code", hole=.3)
    http_requests_fig.layout.template = "plotly_dark"
    return http_requests_fig

@app.callback(
    Output("vus", "figure"),
    Input("date", "value")) 
def generate_chart(date):
    vus_df = get_vus_df(date)
    vus_fig = px.pie(vus_df, title="Virtual Users Results", values="Amount of VUs", names="Status", hole=.3)
    vus_fig.layout.template = "plotly_dark"
    return vus_fig

@app.callback(
    Output("page-performance", "figure"),
    Input("date", "value"), 
    Input("url", "value")) 
def generate_chart(date, url):
    page_performance_df = get_page_performance_df(date)
    color="Metric"
    
    if (url is not None and url != "All"):
        mask = page_performance_df["URL"] == url
        page_performance_df = page_performance_df[mask]
    
    fig = px.bar(page_performance_df, title="Page Performance", x="Response Time (ms)", y="Type", color=color, barmode="group", orientation="h")
    fig.layout.template = "plotly_dark"
    
    return fig

@app.callback(
    Output("vus-session-length", "figure"),
    Input("date", "value")) 
def generate_chart(date):
    vus_session_length_df = get_vus_session_length(date)
    vus_session_length_fig = px.bar(vus_session_length_df, title="Virtual User Session Length", y="Metric", x="Session Length (ms)", color="Metric", orientation="h")
    vus_session_length_fig.layout.template = "plotly_dark"
    return vus_session_length_fig

@app.callback(
    Output("load-summary", "figure"),
    Input("date", "value")) 
def generate_chart(date):
    load_summary_df = get_load_summary(date)
    load_summary_fig = plotly_dual_axis(load_summary_df, load_summary_df, title="Load Summary", y1="Virtual Users", y2="HTTP Requests")
    load_summary_fig.layout.template = "plotly_dark"
    return load_summary_fig

app.run_server(debug=True)