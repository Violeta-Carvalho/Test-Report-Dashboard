import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from os import listdir
from os.path import isfile, join
import json

reportsPath = "./reports/"

def file_by_date(date):
    response = None
    try:
        response = date.strftime("%Y%m%dT%H%M%S") + ".json"
    except:
        response = date.replace(" ", "T").replace(":", "").replace("-", "") + ".json"
    return response

def get_files_in_path():
    onlyfiles = [f for f in listdir(reportsPath) if isfile(join(reportsPath, f))]
    onlyfiles.sort(reverse=True)
    return onlyfiles

def get_report(date):
    file_name = file_by_date(date)
    files = get_files_in_path()
    if len(files) > 0:
        for file in files:
            if file_name == file:
                with open(reportsPath + file) as f:
                    report = json.load(f)
                    return report
    else:
        return None
    
def get_all_reports():
    reports = []
    files = get_files_in_path()
    for file in files:
        with open(reportsPath + file) as f:
            report = json.load(f)
            reports.append(report)
    return reports


def plotly_dual_axis(data1, data2, title="", y1="", y2="", x="Timestamps"):
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig1 = px.line(y=data1[y1], x=data1[x])
    fig2 = px.line(data2[y2], x=data2[x])
    fig2.update_traces(yaxis="y2")

    subplot_fig.add_traces(fig1.data + fig2.data)

    subplot_fig.update_layout(title=title, yaxis=dict(title=y1), yaxis2=dict(title=y2), xaxis=dict(title=x))

    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))


    return subplot_fig

def json_name_to_date(json_name):
    json_name = datetime.strptime(json_name.replace(".json", ""), "%Y%m%dT%H%M%S")
    return json_name

def get_all_dates():
    dates = []
    for f in get_files_in_path():
        dates.append(json_name_to_date(f))
    return dates
