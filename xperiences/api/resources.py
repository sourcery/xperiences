from django.views.decorators.vary import vary_on_headers
from django.db.models.loading import get_model
from backend.models import UserLog, UserMessage

__author__ = 'ishai'

from piston.resource import Resource
from api.handlers import *

OPEN_MODELS = [UserExtension,UserLog,UserMessage,Experience]


def generic_handler(model_param):
    class GenericHandler(MyBaseHandler):
        allowed_methods = ('GET','POST','PUT','DELETE')
        model = model_param

        def read(self,request,*args,**kwargs):
            params = dict([ (k,request.GET[k]) for k in request.GET])
            return super(GenericHandler,self).read(request,*args,**params)
    return GenericHandler

generic_resources = {}
def generic_resource(request, app='backend', model_name='userextension',*args,**kwargs):
    model_type = get_model(app,model_name)
    if not model_type in OPEN_MODELS:
        raise Exception('This model is not open for API')
    if model_type in generic_resources:
        rsrc = generic_resources[model_type]
    else:
        rsrc = Resource(generic_handler(model_type))
        generic_resources[model_type] = rsrc
    return rsrc(request, *args,**kwargs)

experiences_resource = Resource(ExperienceHandler)



