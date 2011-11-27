from django.conf.urls.defaults import *

urlpatterns = patterns('experiences.views',
                       url(r'^$', 'index', name='experience_index'),
                       url(r'^(?P<id>[a-f0-9]+)/$', 'experience_profile', name='experience_profile'),
                       url(r'^add_experience/(?P<id>[a-f0-9]+)/$', 'add_experience', name='add_experience'),
                       url(r'^add_image/(?P<id>[a-f0-9]+)/$', 'add_image_to_experience', name='add_image_to_experience'),
                       url(r'^category/(?P<category>.+)/$', 'experience_by_category', name='experience_category'),
                    )
