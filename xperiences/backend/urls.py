
__author__ = 'ishai'


from django.conf.urls.defaults import *

urlpatterns = patterns('backend.views',
    (r'^test/', 'test'),
    (r'^configurations/', 'configurations'),
)

