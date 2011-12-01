from django import forms
from backend.models import UserExtension

__author__ = 'ishai'

class MerchantForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ('name', 'address','phone_number','description','xp_location')