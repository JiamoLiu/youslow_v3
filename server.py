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


stats_df_lock = threading.Lock()

def append_to_csv(data,csv_file):
    df = pd.DataFrame(columns=data.keys())
    df = df._append([df, pd.DataFrame([data])], ignore_index=True)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=False,mode="a",header=False)
    else:
        df.to_csv(csv_file, index=False,mode="w",header=True)
    
        

@app.route('/', methods=['GET'])
def home():
    return "<h1> TokSlow Server!</p>"



@app.route('/report', methods= ['POST'])
def store_video_param():
    try:
        # data = dict(request.json)
        # data["epoch_time_ms"] = int(time.time() * 1000)
        # filename = data["video_id_and_cpn"].replace(" / ","_").replace(" ","%")+".csv"
        # print(data)
        print("wowowo")
        # with stats_df_lock:
        #     append_to_csv(data, f"{stats_folder}/{filename}")
        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"


app.run(host = "localhost",port = 34543,debug=True)




