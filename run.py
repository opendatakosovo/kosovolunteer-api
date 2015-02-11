from flask import Flask
from bson.objectid import ObjectId
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

    events_json_string = request.data
    events_json_obj = json_util.loads(events_json_string)
    db.events.insert(events_json_obj)
    resp = Response(
        response=json_string,
        mimetype='application/json')
    return resp



@app.route('/register/volunteer', methods=['POST'])
def register_as_volunteer():

    volunteer_json_string = request.data
    volunteer_json_obj = json_util.loads(volunteer_json_string)
    db.volunteers.insert(volunteer_json_obj)
    id_of_volunteer = volunteer_json_obj['eventId']

    db.events.update(
        {"_id": ObjectId(id_of_volunteer)},
        {"$inc":
            {"applicants.applied": 1}
        }
    )   

    resp = Response(
        response=volunteer_json_obj,
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
