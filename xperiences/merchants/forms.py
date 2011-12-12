from django import forms
from backend.models import UserExtension, UserMessage


class MerchantForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ('name', 'address','phone_number','description','xp_location')

class MerchantMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('title','message')