import flask
from flask import request
import pandas
import os.path
from os import path
from flask_cors import CORS
import traceback

from werkzeug.datastructures import RequestCacheControl
import time
import pandas as pd
import threading
import json
import traceback
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
saved_filename = "video_records.csv"


stats_folder = "./stats_data"
status_folder = "./status_data"
quality_folder = "./quality_data"



stats_df_lock = threading.Lock()
status_df_lock = threading.Lock()
quality_df_lock  = threading.Lock()

def append_to_csv(data,csv_file):
    df = pd.DataFrame(columns=data.keys())
    df = df.append(data, ignore_index=True)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=False,mode="a",header=False)
    else:
        df.to_csv(csv_file, index=False,mode="w",header=True)
        

@app.route('/', methods=['GET'])
def home():
    return "<h1>Youslow Server!.</p>"

@app.route('/state', methods= ['POST'])
def store_state_change():
    data = request.json
    platform = data["platform"]
    try:
        if (platform == "youtube"):
            save_youtube_stats(data,status_folder,status_df_lock)
        elif (platform == "netflix"):
            save_netflix_stats(data,stats_folder,status_folder,status_df_lock)


        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"



@app.route('/quality', methods= ['POST'])
def store_quality_change():
    data = request.json
    platform = data["platform"]
    try:
        if (platform == "youtube"):
            save_youtube_stats(data,quality_folder,quality_df_lock)
        elif (platform == "netflix"):
            save_netflix_stats(data,quality_folder,quality_df_lock)


        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"

def save_youtube_stats(data,folder_name,lock):
    data["epoch_time_ms"] = int(time.time() * 1000)
    filename = "youtube"+"_"+data["video_id_and_cpn"].replace(" / ","_").replace(" ","%")+".csv"
    with lock:
        append_to_csv(data, f"{folder_name}/{filename}")

def save_netflix_stats(data,folder_name,lock):
    data["epoch_time_ms"] = int(time.time() * 1000)
    id = data["url"].split("/")[-1]
    filename = "netflix"+"_"+id.replace(" / ","_").replace(" ","%")+".csv"
    with lock:
        append_to_csv(data, f"{folder_name}/{filename}")


@app.route('/report', methods= ['POST'])
def store_video_param():
    data = request.json
    platform = data["platform"]
    try:
        if (platform == "youtube"):
            save_youtube_stats(data,stats_folder,stats_df_lock)
        elif (platform == "netflix"):
            save_netflix_stats(data,stats_folder,stats_df_lock)


        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"


app.run(host = "localhost",port = 34543,debug=True)




