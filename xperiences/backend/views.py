from django.contrib.auth.models import User
from django.core.mail import send_mail
from backend import utils
from backend.forms import SiteConfigurationForm, UserForm, UserExtensionForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from backend.management.commands.ensure_geo_fields import ensure_geo_fields
from django.http import HttpResponse
from backend.models import UserExtension
import settings


def make_admin_view(form_type,template='admin_form.html', success_template='admin_form_saved.html'):

    @user_passes_test(lambda u: u.is_superuser,login_url='/admin/')
    def view(request):
        if request.method == 'GET':
            form = form_type()
            context = {'form' : form }
            return render_to_response(template, context_instance=RequestContext(request, context))
        else:
            form = form_type(request.POST)
            if form.is_valid():
                form.save_data()
                context = { 'message' : 'Settings saved successfuly', 'return_url' : '/admin/', 'return_title' : 'Back to admin home' }
                return render_to_response(success_template,context_instance=RequestContext(request, context ))
            else:
                context = { 'form':form }
                return render_to_response(template, context_instance=RequestContext(request, context))
    return view

configurations = make_admin_view(SiteConfigurationForm)


@user_passes_test(lambda u: u.is_superuser)
def geo_indexes(request):
    return HttpResponse(ensure_geo_fields())


@user_passes_test(lambda u: u.is_superuser,login_url='/admin/')
def preconfigured_merchant(request):
    if request.method == 'GET':
        form_user = UserForm()
        form_user_extension = UserExtensionForm()
        context = {'form_user' : form_user, 'form_user_extension' : form_user_extension }
        return render_to_response('preconfigured_merchant_form.html', context_instance=RequestContext(request, context))
    else:
        user= User()
        user.is_active = False
        form_user = UserForm(request.POST,request.FILES, instance=user)
        if form_user.is_valid():
            form_user.save()
            user_extension = UserExtension.create_from_user(user)
            user_extension.is_merchant = True



            form_user_extension = UserExtensionForm(request.POST,request.FILES,instance=user_extension)

            if form_user_extension.is_valid():
                form_user_extension.save()
                utils.send_email_for_preconfigured_merchant(user_extension)
                context = { 'message' : 'Settings saved successfuly', 'return_url' : '/admin/', 'return_title' : 'Back to admin home' }
                return render_to_response('admin_form_saved.html',context_instance=RequestContext(request, context ))
        else:
            form_user_extension = UserExtensionForm()
            context = {'form_user' : form_user, 'form_user_extension' : form_user_extension }
            return render_to_response('preconfigured_merchant_form.html', context_instance=RequestContext(request, context))

@login_required()
def email_referral(request):
    context = {}
    if request.method == 'POST':
        to = request.POST['to']
        to = to.strip().split(',')
        subject = '%s want\'s to share with you this cool site' % request.user.get_full_name()
        message = request.POST['message']
        message += '\n' + settings.BASE_URL
        message += '?username=' + request.user.username
        send_mail(subject,message,settings.EMAIL_HOST_USER,to)
        context['sent'] = True
    return render_to_response('email_referral.html',context_instance=RequestContext(request,context))

def share(request):
    link = settings.BASE_URL
    if request.user and request.user.is_authenticated():
        link += "?referrer=" + request.user.username
    return render_to_response('share.html',context_instance=RequestContext(request,{'link':link}))