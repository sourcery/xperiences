from django.conf.urls.defaults import *

urlpatterns = patterns('experiences.views',
                       url(r'^$', 'index', name='experience_index'),
                       url(r'^(?P<id>\d+)/$', 'experience_profile', name='experience_profile'),
                       url(r'^/category/(?P<category>[a-z]+)/$', 'experience_by_category', name='experience_category')
                    )