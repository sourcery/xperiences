from django.contrib.auth.models import User
from backend import utils
from backend.decorators import merchant_required
from backend.models import UserExtension, UserMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from experiences.forms import ExperienceForm
from experiences.models import Experience
from merchants.forms import MerchantForm, MerchantMessageForm


def merchant_profile(request, username):
    merchant = UserExtension.get_merchant(user=User.objects.get(username=username))
    template_name = 'merchants/merchant_profile.html'
    return render_to_response(template_name, {'merchant': merchant}, context_instance=RequestContext(request))


@login_required()
def register(request):
    status = ''
    template_name = 'merchants/merchant_application.html'
    merchant = request.user.get_profile()
    merchant.is_merchant = True
    if request.method == 'POST':
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            email = request.POST.get('email')
            if email and email != '' and email != request.user.email:
                request.user.email = email
                request.user.save()
            status = 'saved'
            print "I work!"
            utils.merchant_onreview_email(merchant)
            return render_to_response(template_name, {'form':form,'status': status, 'merchant':merchant}, context_instance=RequestContext(request))
        else:
            errors = form.errors
            status = 'yay! Merchant created'
            print "I work!"
            return render_to_response(template_name, {'form':form,'errors':errors,'status': status, 'merchant':merchant}, context_instance=RequestContext(request))
    else:
        form = MerchantForm(instance=merchant)
        return render_to_response(template_name, {'form':form, 'status': status, 'merchant':merchant}, context_instance=RequestContext(request))


@merchant_required()
def experiences(request):
    if request.method == 'GET':
        return render_to_response('merchants/experiences.html', {'merchant':request.merchant}, context_instance=RequestContext(request))

@merchant_required()
def merchant_inbox(request):
    comments = UserMessage.objects.filter(to=request.merchant)
    return render_to_response('merchants/inbox.html', {'comments' : comments},context_instance=RequestContext(request))



@merchant_required()
def account(request):
    merchant = request.merchant
    if request.method == 'POST':
        form = MerchantForm(request.POST,request.FILES, instance=merchant)
        if form.is_valid():
            form.save()
            return render_to_response('merchants/account.html', {'form':form,'merchant':merchant}, context_instance=RequestContext(request))
        else:
            errors = form.errors
            return render_to_response('merchants/account.html', {'form':form,'errors':errors,'merchant':merchant}, context_instance=RequestContext(request))
    else:
        form = MerchantForm(instance=merchant)
        return render_to_response('merchants/account.html', {'form':form, 'merchant':merchant}, context_instance=RequestContext(request))


@login_required()
def view_message(request,id):
    if request.method == 'GET':
        message = UserMessage.objects.get(id=id)
        return render_to_response('merchants/view_message.html',context_instance=RequestContext(request,{'message':message}))
    else:
        comment = request.POST.get('reply','')
        if comment and comment != '':
            message = UserMessage.objects.get(id=id)
            reply = UserMessage(to=message.sender, sender=message.to, title=message.title,message=comment)
            reply.save()
            return render_to_response('merchants/view_message.html',context_instance=RequestContext(request,{'message':message,'reply':reply,'status':'ok'}))
        else:
            return render_to_response('merchants/view_message.html',context_instance=RequestContext(request,{'message':message,'reply':reply,'status':'no message'}))



@login_required()
def comment_merchant(request,username):
    if request.method == 'GET':
        form = MerchantMessageForm()
        return render_to_response('merchants/comment.html',context_instance=RequestContext(request, {'form':form}))
    else:
        merchant = UserExtension.get_merchant(name=username)
        if merchant:
            msg = UserMessage(to=merchant)
            if request.user_extension:
                msg.sender = request.user_extension
            else:
                msg.sender_session = request.session.session_key
            message = request.POST.get('message')
            form = MerchantMessageForm(request.POST,instance=msg)
            if form.is_valid():
                form.save()
                return HttpResponse('ok sent')
            else:
                return render_to_response('merchants/comment.html',context_instance=RequestContext(request, {'form':form}))
        else:
            return HttpResponse('no such merchant')



@merchant_required()
def edit_experience(request, slug_id):
    exp = Experience.objects.get(slug_id=slug_id)
    if request.method == 'GET':
        form = ExperienceForm(instance=exp)
        return render_to_response('merchants/edit_experience.html', context_instance=RequestContext(request,{'form' : form}) )
    else:
        form = ExperienceForm(request.POST,request.FILES,instance=exp)
        if form.is_valid():
            form.save()
            return HttpResponse('saved')
        else:
            return render_to_response('merchants/edit_experience.html', context_instance=RequestContext(request,{'form' : form}) )



def wrapmongo(o):
    """Lets you access dict.id to get dict._id"""
    class MongoDict(dict):
        def __init__(self, i):
            dict.__init__(self, i)
        @property
        def id(self):
            return str(self.get('_id'))
    if not isinstance(o, dict):
            return (MongoDict(i) for i in o)
    else:
        return MongoDict(o)

