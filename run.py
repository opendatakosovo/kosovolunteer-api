from flask import Flask
from flask import Response, request, jsonify
from bson import json_util, SON
from pymongo import MongoClient
import json
import argparse

mongo = MongoClient()

db = mongo.volunteering
event = db.events

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

@app.route('/display/events', methods=['GET'])
def display_events():

    json = db.events.find({}).sort([("_id", -1)])


    resp = Response(
        response=json_util.dumps(json),
        mimetype='application/json')
    return resp


@app.route('/create/event', methods=['POST'])
def create_event():
    json_doc = {}

    json_string = request.data
    json_obj = json_util.loads(json_string)
    json_obj_name_val = json_obj['name']
    json_obj_description_val = json_obj['description']
    json_obj_volunteer = json_obj['applicants']
    json_obj_from_string = json_util.dumps(json_obj)

    json_doc={
        "name": json_obj_name_val,
        "description": json_obj_description_val,
        "applicants":json_obj_volunteer
    }


    db.events.insert(json_doc)
    
    resp = Response(
        response=json_string,
        mimetype='application/json')
    return resp




@app.route('/register/volunteer', methods=['POST'])
def register_as_volunteer():
    json_doc = {}

    json_string = request.data
    json_obj = json_util.loads(json_string)
    json_obj_event_name_val = json_obj['eventID']
    json_obj_name_val = json_obj['name']
    json_obj_email_val = json_obj['e-mail']
    json_obj_from_string = json_util.dumps(json_obj)

    json_doc={
        "eventID": json_obj_event_name_val,
        "name": json_obj_name_val,
        "e-mail": json_obj_email_val

    }


    db.applyvolunteer.insert(json_doc)

    
    resp = Response(
        response=json_string,
        mimetype='application/json')
    return resp





@app.route('/display/volunteer', methods=['GET'])
def display_volunteer():

    json = db.applyvolunteer.aggregate([{"$group":{
            "_id":{
                "Id":"$eventID"},
                "numriVullnetareve":{"$sum":1}
                    }},
            {"$project":{
            "eventId":"$_id.Id",
            "Numri": "$numriVullnetareve",
            "_id":0

            }}])

    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')
    return resp

if __name__ == '__main__':

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to: [%(default)s].')
    parser.add_argument('--port', type=int, default='5030', help='Port to listen to: [%(default)s].')
    parser.add_argument('--debug', action='store_true', default=True, help='Debug mode: [%(default)s].')

    # Parse arguemnts and run the app.
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
