from django.conf.urls.defaults import *

urlpatterns = patterns('merchants.views',
                       url(r'^(?P<slug>[-\w]+)/$', 'view_merchant_profile', name='merchant_profile'),
                    )