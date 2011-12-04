from django.conf.urls.defaults import *

urlpatterns = patterns('merchants.views',
                       url(r'^register/$', 'register', name='merchant_register'),
                        url(r'^experiences/$', 'experiences', name='merchant_experiences'),
                        url(r'^edit_experience/(?P<id>[a-f0-9]+)/?$', 'edit_experience', name='merchant_edit_experience'),
                       url(r'^(?P<username>[-\w]+)/$', 'merchant_profile', name='merchant_profile'),
                    )