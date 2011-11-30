from django import forms
from models import Experience

__author__ = 'ishai'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ('title', 'description','category','price','video_link','use_saved_address','pub_date','photo1','photo2','photo3','photo4','photo5','xp_location')