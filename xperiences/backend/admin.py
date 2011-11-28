from backend import configurations
from django import forms as django_forms
from experiences.models import Experience


__author__ = 'ishai'

from models import *
from django.contrib import admin

class SiteConfigurationForm(django_forms.forms.Form):

    EXPERIENCE_OF_THE_DAY = django_forms.ModelChoiceField(Experience.objects.all(),'nothing')

    CATEGORIES = django_forms.CharField()

    def __init__(self, data = None):
        if data == None:
            data = configurations.get_dict()
        forms.Form.__init__(self,data)

    def save_data(self):
        configurations.update_configurations(self.data)


admin.site.register(UserExtension)

#admin.site.register(Listing)