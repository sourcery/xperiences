from backend.lite_admin import lite_admin
from django.contrib import admin

from experiences.models import *

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'photo1')


admin.site.register(Experience, ExperienceAdmin)
lite_admin.register(Experience, ExperienceAdmin)