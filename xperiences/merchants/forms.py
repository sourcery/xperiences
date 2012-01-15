from django import forms
from backend.fields import GeoField
from backend.models import UserExtension, UserMessage
from backend.widgets import PointWidgetWithAddressField
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator

class PhoneValidator(RegexValidator):

    def __init__(self, ):
        super(PhoneValidator,self).__init__(regex='^[\d-]+$',message='Phone is not a valid phone number')

class MerchantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MerchantForm, self).__init__(*args, **kwargs)

    def full_clean(self):
        field = self.fields['xp_location']
        field.widget = PointWidgetWithAddressField(address_field='id_address',map_id='hidden_map')()
        phone = self.fields['phone_number']
        phone.validators = [MaxLengthValidator(15),PhoneValidator(),MinLengthValidator(6)]
        return super(MerchantForm,self).full_clean()

    def is_valid(self):
        if super(MerchantForm,self).is_valid():
            if self.data['address'].strip() != u'':
                return True
            self._errors.setdefault('address', self.error_class()).extend(('Please insert address',))
        return False



    class Meta:
        model = UserExtension
        fields = ('name', 'address','phone_number','description','xp_location','photo','offering','target_customers')

class MerchantMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('title','message')