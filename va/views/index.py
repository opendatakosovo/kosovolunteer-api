from flask.views import View

class Index(View):
    methods = ['GET']
    
    def dispatch_request(self):
        return 'Hello'