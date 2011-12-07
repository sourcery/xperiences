from django import forms
from backend.models import UserExtension


class MerchantForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ('name', 'address','phone_number','description','xp_location')