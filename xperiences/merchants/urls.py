from django.conf.urls.defaults import *

urlpatterns = patterns('merchants.views',
                       url(r'^register/$', 'register', name='merchant_register'),
                       url(r'^waiting_approval/$', 'waiting_approval', name='merchant_waiting_approval'),
                       url(r'^experiences/$', 'experiences', name='merchant_experiences'),
                       url(r'^edit_experience/(?P<slug_id>[a-z0-9\-]+)/?$', 'edit_experience', name='merchant_edit_experience'),
                       url(r'^inbox/$', 'merchant_inbox', name='merchant_inbox'),
                       url(r'^account/$', 'account', name='merchant_account'),
                       url(r'^view_message/(?P<id>[a-f0-9]+)/$', 'view_message', name='view_message'),
                       url(r'^comment/(?P<username>[-\w]+)/$', 'comment_merchant', name='comment_merchant'),
                       url(r'^(?P<username>[-\w]+)/$', 'merchant_profile', name='merchant_profile'),
                       url(r'^$', 'experiences', name='merchant_profile'),
                    )