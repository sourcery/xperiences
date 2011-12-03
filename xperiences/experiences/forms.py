from django import forms
from django.forms.fields import DateTimeField
from backend.forms import XPDatePicker
from models import Experience



class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            if isinstance(field,DateTimeField):
                field.widget = XPDatePicker()

    class Meta:
        model = Experience
        exclude = ('merchant','pub_date')
#        fields = ('title', 'description','category','price','video_link','use_saved_address','valid_from','valid_until','pub_date','photo1','photo2','photo3','photo4','photo5','xp_location','tags')