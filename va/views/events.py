from flask import Response
from flask.views import View
from bson import json_util
from va import mongo


class Events(View):
    methods = ['GET']
    
    def dispatch_request(self):
        json = mongo.db.events.find({}).sort([("_id", -1)])

        resp = Response(
            response=json_util.dumps(json),
            mimetype='application/json')

        return resp