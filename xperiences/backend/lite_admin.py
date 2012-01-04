from backend import utils
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from backend.admin import UserExtensionAdmin
from backend.models import UserLog
from experiences.models import Experience, Category
from models import UserExtension


class LiteAdmin(AdminSite):
    pass


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'photo1', 'is_active')

class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user','session','url','time',)
    list_filter = ('user',)

class CategoryAdmin(admin.ModelAdmin):
    pass

lite_admin = LiteAdmin("lite_admin", "lite_admin")
lite_admin.register(UserExtension, UserExtensionAdmin)
lite_admin.register(Experience, ExperienceAdmin)
lite_admin.register(UserLog,UserLogAdmin)
lite_admin.register(Category,CategoryAdmin)