import sorl
from django.contrib import admin
from backend import utils
from backend.models import UserMessage, UserExtension, UserLog, SiteConfiguration
from django.contrib.admin.sites import AdminSite
from django.http import HttpResponseRedirect
from django.utils.functional import update_wrapper
from experiences.models import Experience, Category


class ButtonableModelAdmin(admin.ModelAdmin):
    """
    A subclass of this admin will let you add buttons (like history) in the
    change view of an entry.

    ex.
    class FooAdmin(ButtonableModelAdmin):
       ...

       def bar(self, obj):
          obj.bar()
       bar.short_description='Example button'

       buttons = [ bar ]

    you can then put the following in your admin/change_form.html template:

       {% block object-tools %}
       {% if change %}{% if not is_popup %}
       <ul class="object-tools">
       {% for button in buttons %}
          <li><a href="{{ button.func_name }}/">{{ button.short_description }}</a></li>
       {% endfor %}
       <li><a href="history/" class="historylink">History</a></li>
       {% if has_absolute_url %}<li><a href="../../../r/{{ content_type_id }}/{{ object_id }}/" class="viewsitelink">View on site</a></li>{% endif%}
       </ul>
       {% endif %}{% endif %}
       {% endblock %}

    """
    buttons=[]

    def change_view(self, request, object_id, extra_context={}):
        extra_context['extra_buttons']=[{'func_name':b.func_name, 'short_description':b.short_description} for b in self.buttons]
        return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context)


    def button_view(self, request, object_id,button=None,**kwargs):
        obj = self.model._default_manager.get(pk=object_id)
        button(self,obj)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(button):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(self.button_view)(*args,button=button,**kwargs)
            return update_wrapper(wrapper, button)

        info = self.model._meta.app_label, self.model._meta.module_name
        urlpatterns = patterns('',)
        for button in self.buttons:
            urlpatterns += patterns('',
                url(r'^(.+)/' + button.func_name + '/$',wrap(button),name='%s_%s_' % info  + button.func_name)
                ,)
        urlpatterns += super(ButtonableModelAdmin,self).get_urls()
        return urlpatterns



def approve_merchant(modeladmin, request, queryset):
    for merchant in queryset:
        if merchant.is_merchant and not merchant.is_approved:
            utils.approve_merchant(merchant)


merchant_actions = [approve_merchant]



class UserExtensionAdmin(ButtonableModelAdmin):
    list_display = ('name', 'user', 'photo', 'FB_token', 'is_merchant', 'is_approved','is_deleted')
    actions = merchant_actions
    list_filter = ('is_merchant', 'is_approved','is_deleted')

    def approve(self, obj):
        utils.approve_merchant(obj)
    approve.short_description = 'Approve (Send Email)'
    buttons = [approve]



class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'photo1', 'is_active', 'merchant')



class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user','session','url','time',)
    list_filter = ('user',)



class CategoryAdmin(admin.ModelAdmin):
    pass



class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('to', 'sender', 'time',)
    list_filter = ('to', 'sender', 'time',)


super_admin = admin.site
try:
    super_admin.register(UserLog, UserLogAdmin)
    super_admin.register(sorl.thumbnail.models.KVStore)
    super_admin.register(UserExtension, UserExtensionAdmin)
    super_admin.register(UserMessage, UserMessageAdmin)
except Exception:
    pass



class LiteAdmin(AdminSite):
    _registry = {}


lite_admin = LiteAdmin("lite_admin")
lite_admin.register(UserExtension, UserExtensionAdmin)
lite_admin.register(Experience, ExperienceAdmin)
lite_admin.register(UserLog, UserLogAdmin)
lite_admin.register(Category, CategoryAdmin)
lite_admin.register(UserMessage, UserMessageAdmin)