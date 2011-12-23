from django import forms
from backend.fields import GeoField
from backend.models import UserExtension, UserMessage
from backend.widgets import PointWidgetWithAddressField


class MerchantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MerchantForm, self).__init__(*args, **kwargs)
        field = self.fields['xp_location']
        field.widget = PointWidgetWithAddressField(address_field='id_address',map_id='hidden_map')()

    class Meta:
        model = UserExtension
        fields = ('name', 'address','phone_number','description','xp_location','photo')

class MerchantMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('title','message')