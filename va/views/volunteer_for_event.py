from flask import Response, request
from flask.views import View
from bson import json_util, ObjectId
from va import mongo


class VolunteerForEvent(View):
    methods = ['POST']

    def dispatch_request(self):

        volunteer_json_string = request.data
        volunteer_json_obj = json_util.loads(volunteer_json_string)

        # Create volunteer doc
        mongo.db.volunteers.insert(volunteer_json_obj)

        # Increment event attendance
        event_id = volunteer_json_obj['eventId'] 
        mongo.db.events.update(
            { '_id': ObjectId(event_id) },
            { '$inc': { 'applicants.applied': 1 }}
        )
        
        resp = Response(status=200, mimetype='application/json')
        return resp