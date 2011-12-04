from backend.admin import SiteConfigurationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'ishai'

def make_admin_view(form_type,template='admin_form.html', success_template='admin_form_saved.html'):

    @user_passes_test(lambda u: u.is_superuser)
    def view(request):
        if request.method == 'GET':
            form = form_type()
            context = {'form' : form }
            return render_to_response(template, context_instance=RequestContext(request, context))
        else:
            form = form_type(request.POST)
            form.save_data()
            context = { 'message' : 'Settings saved successfuly', 'return_url' : '/admin/', 'return_title' : 'Back to admin home' }
            return render_to_response(success_template,context_instance=RequestContext(request, context ))
    return view

configurations = make_admin_view(SiteConfigurationForm)

def test(request):
    return render_to_response('test.html')