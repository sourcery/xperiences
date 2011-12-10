from django.conf.urls.defaults import *
from backend import views

urlpatterns = patterns('',
    (r'^test/', views.test),
    (r'^geo_indexes/', views.geo_indexes),
    (r'^configurations/', views.configurations),
    (r'^create_merchant/', views.preconfigured_merchant),

)

