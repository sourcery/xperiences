from django.conf.urls.defaults import *

urlpatterns = patterns('experiences.views',
                       url(r'^$', 'index', name='experiences_index'),
                       url(r'^(?P<id>\d+)/$', 'experience_profile', name='experience_profile'),
                    )