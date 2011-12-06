from django.http import HttpResponse

class operation_failed_response ( HttpResponse):
    def __init__(self, msg = ''):
        HttpResponse.__init__(self,"operation failed: " + msg, mimetype='text/plain')

class no_premission_response( HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self,"You need higher permission for this operation", mimetype='text/plain')

class ok_response ( HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self,"ok", mimetype='text/plain')

class json_response(HttpResponse):
    def __init__(self, json=None):
        if not json: json = {}
        HttpResponse.__init__(self,json.dumps(json), mimetype='application/json')

class message_response(HttpResponse):
    def __init__(self, msg = ''):
        HttpResponse.__init__(self,msg, mimetype='text/plain')
