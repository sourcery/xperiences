
__author__ = 'ishai'


from django.conf.urls.defaults import *
from backend.resources import  *

urlpatterns = patterns('backend.views',
    (r'^configurations/', 'configurations'),
)

