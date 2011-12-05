from backend import utils
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
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

lite_admin = LiteAdmin("lite_admin", "lite_admin")
lite_admin.register(UserExtension, UserExtensionAdmin)

import sorl

lite_admin.register(sorl.thumbnail.models.KVStore)