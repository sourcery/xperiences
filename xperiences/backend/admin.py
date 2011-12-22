from backend.models import UserMessage
from models import UserExtension, UserLog, SiteConfiguration
from django.contrib import admin


admin.site.register(UserExtension)
admin.site.register(UserLog)
admin.site.register(SiteConfiguration)
import sorl

admin.site.register(sorl.thumbnail.models.KVStore)

admin.site.register(UserMessage)

