from flask import Response, request
from flask.views import View
from bson import json_util
from va import mongo


class DeleteEvent(View):
    methods = ['POST']

    def dispatch_request(self):

        event_json_string = request.data
        event_json_obj = json_util.loads(event_json_string)

        event_id = event_json_obj['eventId'] 

        mongo.db.events.remove({'_id': ObjectId(event_id)})
        
        resp = Response(status=200, mimetype='application/json')
        return resp