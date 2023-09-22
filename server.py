import flask
from flask import request
import pandas
import os.path
from os import path
from flask_cors import CORS
import traceback

from werkzeug.datastructures import RequestCacheControl

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


dataframe_lock = threading.Lock()

def append_to_csv(data,csv_file):
    with dataframe_lock:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            df = pd.DataFrame(columns=data.keys())

        df = df.append(data, ignore_index=True)
        df.to_csv(csv_file, index=False)
        

@app.route('/', methods=['GET'])
def home():
    return "<h1>Youslow Server!.</p>"



@app.route('/report', methods= ['POST'])
def store_video_param():
    try:
        data = request.json
        filename = data["video_id_and_cpn"].replace(" / ","_").replace(" ","%")+".csv"
        append_to_csv(data, f"{stats_folder}/{filename}")
        return "OK"
    except Exception as e:
        traceback.print_exc()
        return "ERROR"


app.run(host = "localhost",port = 34543,debug=True)




