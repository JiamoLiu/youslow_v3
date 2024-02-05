import flask
from flask import request
import pandas
import os.path
from os import path
from flask_cors import CORS
import traceback

import time
import pandas as pd
import threading
import json
import traceback
from werkzeug.datastructures import RequestCacheControl
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



@app.route('/report', methods= ['POST', 'OPTIONS'])
def store_video_param():
    data = request.json
    platform = data["platform"]
    print(data)
    try:
        print(data)
        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = 34543)



