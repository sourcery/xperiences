from django.contrib import admin

from experiences.models import *

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


admin.site.register(Experience, ExperienceAdmin)