
__author__ = 'ishai'


from django.conf.urls.defaults import *
from api.resources import  *

urlpatterns = patterns('api.views',
    (r'^experiences/(?P<emitter_format>(json|xml))$', experiences_resource),
    (r'^message/((?P<id>[0-9a-z]+)/)?(?P<emitter_format>(json|xml))$', message_resource),
    (r'^(?P<app>.+)/(?P<model_name>.+)/(?P<emitter_format>(json|xml))$', generic_resource),
    (r'^test/', 'test'),
)

