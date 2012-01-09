from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
#noinspection PyDeprecation
from django.views.generic.simple import direct_to_template
from backend.admin import lite_admin, super_admin
admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),


    (r'^experiences/', include('experiences.urls')),
    (r'^merchants/login/$', 'socialauth.views.merchant_login_page'),
    (r'^merchants/', include('merchants.urls')),
    (r'^api/', include('api.urls')),
    (r'^admin/backend/', include('backend.urls')),
    (r'^accounts/', include('socialauth.urls')),
    (r'^super_admin/', include(super_admin.urls)),
    (r'^admin/', include(lite_admin.urls)),
    (r'^about', direct_to_template, {'template': 'about.html'}),
    (r'^jobs', direct_to_template, {'template': 'jobs.html'}),
    (r'^terms', direct_to_template, {'template': 'terms.html'}),
    (r'^share', 'backend.views.share'),
	(r'^email_referral', 'backend.views.email_referral'),
	(r'^fb_referral', 'backend.views.invite'),
    (r'^facebook/','backend.views.invite_callback'),
    (r'^start', direct_to_template, {'template': 'start.html'}),
    (r'^contact', direct_to_template, {'template': 'contact.html'}),
    (r'^user', 'backend.views.user_inbox'),
    (r'^$', include('experiences.urls')),

) + static(settings.MEDIA_URL, document_root=settings.STATIC_DOC_ROOT)
