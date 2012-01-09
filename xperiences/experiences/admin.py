from backend.admin import ExperienceAdmin
from django.contrib import admin

from experiences.models import *

admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Category)