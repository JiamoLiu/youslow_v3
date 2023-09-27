import flask
from flask import request, render_template_string, jsonify
import pandas
import os.path
from os import path
from flask_cors import CORS
import traceback

from werkzeug.datastructures import RequestCacheControl

app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) #cross origin something server
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
saved_filename = "video_records.csv"

fun = "Wowie"
template = """
<!DOCTYPE html>
<html>
<head>
    <title>YouSlow!</title>
    <body>
        <h1>YouSlow! {{ fun }}</h1>
    </body>
</head>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(template, fun=fun)

@app.route('/report', methods= ['GET']) # Since it is post, you can't see anything unless info is present
def store_video_param():
    try:
        raw_data = request.get_data(as_text=True)
        temp = dict(request.args)
        # temp["raw"] = raw_data
        # temp["loaded_fractions"] = request.get_json()["bufferFraction"]
        # temp["playback_fractions"] = request.get_json()["playbackSeries"]
        # temp["codec_instants"] = request.get_json()["codecInstants"]
        # temp["dimension_frame_instants"]= request.get_json()["dimensionFrameInstants"]
        # temp["bandwidth_kbps_instants"] = request.get_json()["bandwidthKbpsInstants"]
        # temp["buffer_health_seconds_instants"] = request.get_json()["bufferHealthSecondsInstants"]
        # temp["debug_info_instants"] = request.get_json()["debugInfoInstants"]
        # temp["network_activity_bytes_instants"] =  request.get_json()["networkActivityBytesInstants"]
        # temp["resolution_instants"] = request.get_json()["resolutionInstants"]
        # temp["player_states"] = request.get_json()["playerStates"]
        # print(temp["stats_for_nerds"])
        # print(temp["stats_for_nerds"][0])
        # temp["raw_data"] = raw_data
        # df = pandas.DataFrame([temp])
        # #print(df)
        # if (path.exists(saved_filename)):
        #     df.to_csv(saved_filename,header=False, mode='a', index=False,encoding='utf-8')
        # else:
        #     df.to_csv(saved_filename,index=False,encoding='utf-8')
        return jsonify(temp)
    except:
        traceback.print_exc()
        return "ERROR!"
    
@app.route('/submit', methods=['POST'])
def submit_form():
    fun = "bruh"
    # Process the submitted data and perform actions
    return f'Data received and processed'


app.run(host = "localhost", port=34543,debug=False)




