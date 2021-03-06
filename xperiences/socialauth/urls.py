from django.conf.urls.defaults import *
from openid_consumer.views import complete, signout
from django.views.generic.simple import direct_to_template

#Login Views
urlpatterns = patterns('socialauth.views',
    url(r'^login/$', 'login_page', name='socialauth_login_page'),
    url(r'^logout/$', 'social_logout', name='socialauth_social_logout'),
    url(r'^sign_in/$', 'sign_in', name='socialauth_social_sign_in'),
    url(r'^inactive/$', 'inactive', name='socialauth_inactive'),
    url(r'^validate/$', 'validate', name='socialauth_validate'),
    url(r'^login_success/$', 'login_success', name='socialauth_login_success'),

    url(r'^facebook_login/xd_receiver.htm$', direct_to_template, {'template':'xd_receiver.htm'}, name='socialauth_xd_receiver'),
    url(r'^facebook_login/$', 'facebook_login', name='socialauth_facebook_login'),
    url(r'^facebook_login/done/$', 'facebook_login_done', name='socialauth_facebook_login_done'),
    url(r'^openid_login/$', 'openid_login_page', name='socialauth_openid_login_page'),
    url(r'^twitter_login/$', 'twitter_login', name='socialauth_twitter_login'),
    url(r'^twitter_login/done/$', 'twitter_login_done', name='socialauth_twitter_login_done'),
    url(r'^linkedin_login/$', 'linkedin_login', name='socialauth_linkedin_login'),
    url(r'^linkedin_login/done/$', 'linkedin_login_done', name='socialauth_linkedin_login_done'),
    url(r'^yahoo_login/$', 'yahoo_login', name='socialauth_yahoo_login'),
    url(r'^yahoo_login/complete/$', complete, name='socialauth_yahoo_complete'),
    url(r'^gmail_login/$', 'gmail_login', name='socialauth_google_login'),
    url(r'^gmail_login/complete/$', complete, name='socialauth_google_complete'),
    url(r'^openid/$', 'openid_login', name='socialauth_openid_login'),
    url(r'^openid/complete/$', complete, name='socialauth_openid_complete'),
    url(r'^openid/signout/$', signout, name='openid_signout'),
    url(r'^openid/done/$', 'openid_done', name='openid_openid_done'),
)

