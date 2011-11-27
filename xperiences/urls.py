from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import socialauth.urls

#urlpatterns =  patterns('',(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#       {'document_root': settings.STATIC_DOC_ROOT}))

urlpatterns = patterns('', 
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

     (r'^experiences/', include('experiences.urls')),
    
    (r'^merchants/', include('merchants.urls')),

    (r'^accounts/', include(socialauth.urls)),
     #Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^about', direct_to_template, {'template': 'about.html'}),
    
    (r'^$', include('experiences.urls')),
        
) + static(settings.MEDIA_URL, document_root=settings.STATIC_DOC_ROOT)
