from django.contrib import admin

from experiences.models import *

<<<<<<< HEAD
admin.site.register(Experience)
=======
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


admin.site.register(Experience, ExperienceAdmin)
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a
