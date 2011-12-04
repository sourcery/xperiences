from backend import configurations, utils
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
        super(SiteConfigurationForm,self).__init__(data)

    def save_data(self):
        configurations.update_configurations(self.data)

def approve_merchant(modeladmin, request, queryset):
    for merchant in queryset:
        if merchant.is_merchant and not merchant.is_approved:
            utils.approve_merchant(merchant)

merchant_actions = [approve_merchant]
class UserExtensionAdmin(admin.ModelAdmin):
    actions = merchant_actions

admin.site.register(UserExtension,UserExtensionAdmin)

admin.site.register(UserLog)

import sorl

admin.site.register(sorl.thumbnail.models.KVStore)