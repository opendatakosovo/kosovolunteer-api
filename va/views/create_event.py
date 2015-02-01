from flask import Response, request
from flask.views import View
from bson import json_util
from va import mongo


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

class CreateEvent(View):
    methods = ['POST']

    def dispatch_request(self):

        event_json_string = request.data
        event_json_obj = json_util.loads(event_json_string)

        # if no image was given for the event, display a random image.
        # this is for demo purposes
        if event_json_obj['imageUrl'] == '':
            event_json_obj['imageUrl'] = random_event_pics[randint(0,len(random_event_pics)-1)]

        mongo.db.events.insert(event_json_obj)
        
        resp = Response(status=200, mimetype='application/json')
        return resp