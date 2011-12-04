
__author__ = 'ishai'


from django.conf.urls.defaults import *
from api.resources import  *

urlpatterns = patterns('api.views',
    (r'^experiences/(?P<emitter_format>.*)$', experiences_resource),
    (r'^test/', 'test'),
)

