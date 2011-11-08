from django.conf.urls.defaults import *

urlpatterns = patterns('merchants.views',
                       url(r'^register/$', 'register', name='merchant_register'),
                       url(r'^(?P<username>[-\w]+)/$', 'merchant_profile', name='merchant_profile'),
                    )