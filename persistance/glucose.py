from pymongo import MongoClient
from flask import jsonify


class GlucoseValuesDB:
    def __init__(self, app):
        if app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] != '' and app.config['NIGHTSCOUT_DB_NAME'] != '':
            MONGO_CLIENT = MongoClient(app.config['NIGHTSCOUT_DB_CONNECTION_STRING'])
            db = MONGO_CLIENT[app.config['NIGHTSCOUT_DB_NAME']]
            self.collection = db['entries']
        else:
            print("Missing Nightscout Connection String")

    def last_glucose_value(self):
        if self.collection is None:
            # return nothing because no db connection
            return jsonify()
        # ordering of sort matters and dicts in python are unordered so dont use dict for sort
        res = self.collection.find_one(sort=[("_id", -1)])
        # handle errors!
        return jsonify(sgv=res['sgv'],
                       date=res['date'],
                       dateString=res['dateString'],
                       trend=res['trend'],
                       direction=res['direction'])