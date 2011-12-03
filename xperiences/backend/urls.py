from django.conf.urls.defaults import *
from backend import views

urlpatterns = patterns('',
    (r'^test/', views.test),
    (r'^configurations/', views.configurations),
)

