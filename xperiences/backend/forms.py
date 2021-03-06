import random
from django.contrib.auth.models import User
import django.forms as django_forms
import json

import settings


from db_manage import db

def get_all_experiences_as_choices():
    all = db.experience.find({'is_active':True})
    return [(str(e['_id']), str(e['title'])) for e in all]

class SiteConfigurationForm(django_forms.forms.Form):
#    CATEGORIES = django_forms.CharField()
    EXPERIENCE_OF_THE_DAY = django_forms.ChoiceField(get_all_experiences_as_choices())

    def __init__(self, data=None):
        from backend import configurations
        if data is None:
            data = configurations.config
#            data['CATEGORIES'] = json.dumps(data['CATEGORIES'])
        super(SiteConfigurationForm, self).__init__(data)


    def save_data(self):
        from backend import configurations
#        categories = self.data['CATEGORIES']
#        if not categories.startswith('['):
#            categories = '[' + categories
#        if not categories.endswith(']'):
#            categories += ']'
#        self.data['CATEGORIES'] = json.loads(categories)
        configurations.update_configurations(self.data)

#class PreconfiguredMerchant(django_forms.Form):
#    email = django_forms.CharField(required=True)
#    username = django_forms.CharField()
#
#    def is_valid(self):
#        email = self.data['email']
#        username = self.data.get('username',email)
#        exists = User.objects.filter(username=username).count() > 0 or User.objects.filter(email=email).count() > 0
#        return not exists
#
#
#    def save_data(self):
#        from backend import utils
#        from backend.models import UserExtension
#        email = self.data['email']
#        username = self.data.get('username',email)
#        password = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in xrange(12)])
#        user = User(username=username, email=email,password=password)
#        user.is_active = False
#        user.save()
#        ext = UserExtension.create_from_user(user)
#        ext.is_merchant = True
#        ext.save()
#        return user

class UserForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name')

    def save(self, commit=True):
        email = self.data['email']
        username = self.data.get('username',email)
        self.data['username'] = username
        self.data['password'] = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in xrange(12)])
        super(UserForm,self).save(commit=commit)

class UserExtensionForm(django_forms.ModelForm):
    class Meta:
        from backend.models import UserExtension
        model = UserExtension
        fields = ('xp_location','address','is_approved','referred_by','credit','description','phone_number')
