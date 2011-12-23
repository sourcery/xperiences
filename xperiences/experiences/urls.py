from django.conf.urls.defaults import *

urlpatterns = patterns('experiences.views',
                       url(r'^$', 'index', name='experience_index'),
                       url(r'^list/$', 'list_view', name='experience_list'),
                       url(r'^search_test/$', 'search_experience', name='search_experience'),
                       url(r'^add_experience/$', 'add_experience', name='add_experience'),
                       url(r'^category/(?P<category>.+)/$', 'experience_by_category', name='experience_category'),
                       url(r'^(?P<id>[a-zA-Z0-9\-_]+)/$', 'experience_profile', name='experience_profile'),
                    )
