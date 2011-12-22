from backend import utils
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from backend.models import UserLog
from experiences.models import Experience
from models import UserExtension


class LiteAdmin(AdminSite):
    pass


def approve_merchant(modeladmin, request, queryset):
    for merchant in queryset:
        if merchant.is_merchant and not merchant.is_approved:
            utils.approve_merchant(merchant)


merchant_actions = [approve_merchant]


class UserExtensionAdmin(admin.ModelAdmin):
    actions = merchant_actions

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'photo1', 'is_active')

class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user','session','url','time',)
    list_filter = ('user',)

lite_admin = LiteAdmin("lite_admin", "lite_admin")
lite_admin.register(UserExtension, UserExtensionAdmin)
lite_admin.register(Experience, ExperienceAdmin)
lite_admin.register(UserLog,UserLogAdmin)