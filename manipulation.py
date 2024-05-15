from utils import get_report
import pandas as pd
import datetime

def get_vus_df(date):
    report = get_report(date)
    counters = report["aggregate"]["counters"]
    vus_dict = { 
        "Status": ["Completed", "Failed"],
        "Amount of VUs": [counters["vusers.completed"], counters["vusers.failed"]]
    }
    
    df = pd.DataFrame(vus_dict)        
    return df

def get_http_requests_df(date):
    report = get_report(date)
    http_requests_dict = { "Response Code": [], "Amount of Requests": []}
    counters = report["aggregate"]["counters"]
    
    for key, value in counters.items():
        if "browser.page.codes." in key:
            code = key.split("browser.page.codes.")[1]
            http_requests_dict["Response Code"].append(code)
            http_requests_dict["Amount of Requests"].append(value)
            
    df = pd.DataFrame(http_requests_dict)
    return df

def get_page_performance_df(date):
    baseUrl = "https://platform-stage.traivefinance.com"
    report = get_report(date)
    page_performance_dict = { "URL": [], "Response Time (ms)": [], "Type": [], "Metric": [] }
    summaries = report["aggregate"]["summaries"]
    
    for key, value in summaries.items():
        if "browser.page." in key and "#state=" not in key:
            key = key.split("browser.page.")[1].split(".", 1)
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["mean"])
            page_performance_dict["Metric"].append("Mean")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["min"])
            page_performance_dict["Metric"].append("Minimum")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["median"])
            page_performance_dict["Metric"].append("Median")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["p75"])
            page_performance_dict["Metric"].append("Percentile 75")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["p90"])
            page_performance_dict["Metric"].append("Percentile 90")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["p95"])
            page_performance_dict["Metric"].append("Percentile 95")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["p99"])
            page_performance_dict["Metric"].append("Percentile 99")
            
            page_performance_dict["Type"].append(key[0])
            page_performance_dict["URL"].append(key[1].replace(baseUrl, ""))
            page_performance_dict["Response Time (ms)"].append(value["max"])
            page_performance_dict["Metric"].append("Maximum")
        
    df = pd.DataFrame(page_performance_dict)
    return df

def get_vus_session_length(date):
    report = get_report(date)
    session_length_dict = { "Session Length (ms)": [], "Metric": [] }
    session_length = report["aggregate"]["summaries"]["vusers.session_length"]
    
    session_length_dict["Session Length (ms)"].append(session_length["mean"])
    session_length_dict["Metric"].append("Mean")
    
    session_length_dict["Session Length (ms)"].append(session_length["min"])
    session_length_dict["Metric"].append("Minimum")
    
    session_length_dict["Session Length (ms)"].append(session_length["median"])
    session_length_dict["Metric"].append("Median")
    
    session_length_dict["Session Length (ms)"].append(session_length["p75"])
    session_length_dict["Metric"].append("Percentile 75")
    
    session_length_dict["Session Length (ms)"].append(session_length["p90"])
    session_length_dict["Metric"].append("Percentile 90")
    
    session_length_dict["Session Length (ms)"].append(session_length["p95"])
    session_length_dict["Metric"].append("Percentile 95")
    
    session_length_dict["Session Length (ms)"].append(session_length["p99"])
    session_length_dict["Metric"].append("Percentile 99")
    
    session_length_dict["Session Length (ms)"].append(session_length["max"])
    session_length_dict["Metric"].append("Maximum")
    
    df = pd.DataFrame(session_length_dict)
    return df

def get_load_summary(date):
    report = get_report(date)
    load_summary_dict = { "Virtual Users": [], "HTTP Requests": [], "Timestamps": [] }
    intermediates = report["intermediate"]
    totalVusers = 0
    
    for intermediate in intermediates:
        try:
            createdVusers = intermediate["counters"]["vusers.created"]
            totalVusers += createdVusers
        except KeyError:
            pass
        
        try:
            completedVusers = intermediate["counters"]["vusers.completed"]
            totalVusers -= completedVusers
        except KeyError:
            pass
        
        try:
            failedVusers = intermediate["counters"]["vusers.failed"]
            totalVusers -= failedVusers
        except KeyError:
            pass
        

        load_summary_dict["Virtual Users"].append(totalVusers)
        
        firstCounterDate = intermediate["firstCounterAt"]
        firstCounterDate = datetime.datetime.fromtimestamp(firstCounterDate / 1e3)
        load_summary_dict["Timestamps"].append(firstCounterDate)
        
        httpRequestRate = intermediate["counters"]["browser.http_requests"]
        load_summary_dict["HTTP Requests"].append(httpRequestRate)
        
    df = pd.DataFrame(load_summary_dict)
    return df