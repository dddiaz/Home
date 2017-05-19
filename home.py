import os
from pymongo import MongoClient
from flask import Flask, render_template, jsonify


app = Flask(__name__)
app.config.from_object(__name__)

# configs
app.config['FLASK_IN_DEBUG_MODE'] = os.getenv('FLASK_IN_DEBUG_MODE', 'False') == 'True'
app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] = os.getenv('NIGHTSCOUT_DB_CONNECTION_STRING','')
app.config['NIGHTSCOUT_DB_NAME'] = os.getenv('NIGHTSCOUT_DB_NAME','')

# Nightscout db logic
# TODO: move this out
client = None
if app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] != '' and app.config['NIGHTSCOUT_DB_NAME'] != '':
    client = MongoClient(app.config['NIGHTSCOUT_DB_CONNECTION_STRING'])
    db = client[app.config['NIGHTSCOUT_DB_NAME']]
    collection = db['entries']


# TODO back db cli method


@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/test-error')
# def test_error():
#     # Just using this to quickly test that prod isn't in debug mode
#     raise OSError


@app.route('/last-blood-glucose')
def last_blood_glucose():
    if (client == None):
        # return nothing because no db connection
        return jsonify()
    #TODOOOOOOO
    # update sort order!
    # ordering of sort matters and dicts in python are unordered so dont use dict for sort
    res = collection.find_one(sort=[("_id",-1)])
    # handle errors!
    return jsonify(sgv=res['sgv'],
                   date=res['date'],
                   dateString=res['dateString'],
                   trend=res['trend'],
                   direction=res['direction'])


if __name__ == '__main__':
    # Need to set host to access outside of container
    app.run(debug=app.config['FLASK_IN_DEBUG_MODE'], host='0.0.0.0')
