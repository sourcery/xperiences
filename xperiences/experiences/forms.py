from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.fields import DateTimeField
from backend.widgets import XPDatePicker, PointWidgetWithAddressField
from models import Experience



class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        field = self.fields['xp_location']
        field.widget = PointWidgetWithAddressField(address_field='id_address',map_id='hidden_map')()
        for name,field in self.fields.items():
            if isinstance(field,DateTimeField):
                field.widget =  AdminSplitDateTime()

    class Meta:
        model = Experience
        exclude = ('merchant','pub_date','is_active')
#        fields = ('title', 'description','category','price','video_link','use_saved_address','valid_from','valid_until','pub_date','photo1','photo2','photo3','photo4','photo5','xp_location','tags')