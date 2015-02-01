from flask import Flask
from flask import Response, request, jsonify
from bson import json_util, SON, ObjectId
from pymongo import MongoClient
import json
import argparse
from random import randint

mongo = MongoClient()

db = mongo.volunteering
event = db.events

app = Flask(__name__)

# if no image was given for the event, display a random image.
# this is for demo purposes
random_event_pics = [
    'http://www.asgoodasgrass.co.uk/wp-content/gallery/corporate-events-gallery/event-flooring-05.jpg',
    'http://visionevents.co.uk/wp-content/uploads/2012/09/event-production-quirky1.jpg',
    'http://www.revelryeventdesigners.com/wp-content/uploads/2012/08/Revelry-Event-Design-Dina-Douglas-Sonia-Sharma.jpg',
    'http://www.ketchum.com/sites/default/files/styles/media_640w/public/event_marketing.jpg',
    'http://www.wbspecialevents.com/wp-content/uploads/sites/5/2014/05/main-home-page-5.jpg',
    'http://www.grey-hare.co.uk/wp-content/uploads/2012/09/Event-management.png',
    'http://www.holland.com/upload_mm/6/0/0/960_fullimage_amsterdam%20dance%20event%20dj%20club_560x350.jpg',
    'http://www.cellspace.org/new/sites/default/files/CELLspaceEvent.jpg',
    'http://www.drive-intheatre.com.au/wp-content/uploads/2014/08/event_party.jpg',
    'https://40.media.tumblr.com/de58695f875ed2ccafebf79ac9d021cd/tumblr_nh1geev9yI1qzz7ldo1_500.png',
    'https://themixedculturedotcom.files.wordpress.com/2013/09/masskara-festival.jpg',
    'http://ballinnn.com/wp-content/uploads/2014/03/unnamed-4.jpg',
    'http://i.kinja-img.com/gawker-media/image/upload/s--7ZJ5S8Ot--/yyl91baaymht2q2acwru.jpg',
    'http://i.ytimg.com/vi/hQB4NUWTJ4A/maxresdefault.jpg',
    'http://billboardavenue.net/wp-content/uploads/2014/03/festival1.jpg',
    'http://eu.festivalawards.com/wp-content/uploads/20120727_tml12-kevin_018-9225.jpg',
    'http://eu.festivalawards.com/wp-content/uploads/Two-Days-A-Week-Festival.jpg',
    'http://www.blackballad.co.uk/wp-content/uploads/2014/06/Sem_t%C3%ADtulo_holi_festival_colours_2013.jpg',
    'http://www.newrockstarphilosophy.com/wp-content/uploads/2014/04/8541725920_01c18d10e3_b.jpg'
    ]


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

    event_json_string = request.data
    event_json_obj = json_util.loads(event_json_string)

    # if no image was given for the event, display a random image.
    # this is for demo purposes
    print len(random_event_pics)
    if event_json_obj['imageUrl'] == '':
        event_json_obj['imageUrl'] = random_event_pics[randint(0,len(random_event_pics)-1)]

    db.events.insert(event_json_obj)
    
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/delete/event', methods=['POST'])
def delete_event():

    event_json_string = request.data
    event_json_obj = json_util.loads(event_json_string)

    event_id = event_json_obj['eventId'] 
    print ObjectId(event_id)
    db.events.remove({'_id': ObjectId(event_id)})
    
    resp = Response(status=200, mimetype='application/json')
    return resp



@app.route('/register/volunteer', methods=['POST'])
def register_as_volunteer():

    volunteer_json_string = request.data
    volunteer_json_obj = json_util.loads(volunteer_json_string)

    # Create volunteer doc
    db.volunteers.insert(volunteer_json_obj)

    # Increment event attendance
    event_id = volunteer_json_obj['eventId'] 
    db.events.update(
        { '_id': ObjectId(event_id) },
        { '$inc': { 'applicants.applied': 1 }}
    )
    
    resp = Response(status=200, mimetype='application/json')
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
