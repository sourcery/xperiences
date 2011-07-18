from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns =  patterns('',(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': settings.STATIC_DOC_ROOT}))

urlpatterns += patterns('', 
    # Example:
    # (r'^Experience/', include('Experience.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    

    (r'^experiences/', include('experiences.urls')),
    
    (r'^merchants/', include('merchants.urls')),



     #Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    
)