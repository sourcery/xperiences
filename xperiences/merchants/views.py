from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from backend import utils
from backend.decorators import merchant_required
from backend.models import UserExtension
from django.shortcuts import render_to_response
from django.template import RequestContext  # I still need to understand better the concept of RequestContext
#from experiences.models import Experience
#from merchants.models import Merchant
from merchants.forms import MerchantForm


def merchant_profile(request, username):
    merchant = UserExtension.get_merchant(user=User.objects.get(username=username))
    template_name = 'merchants/merchant_profile.html'
    return render_to_response(template_name, {'merchant': merchant}, context_instance=RequestContext(request))


@merchant_required()
def register(request):
    status = ''
    template_name = 'merchants/register.html'
    if request.method == 'POST':
        form = MerchantForm(request.POST,instance=request.merchant)
        if form.is_valid():
            form.save()
            status = 'yay! Merchant created'
            print "I work!"
            utils.merchant_onreview_email(request.merchant)
            return render_to_response(template_name, {'form':form,'status': status, 'merchant':request.merchant}, context_instance=RequestContext(request))
        else:
            errors = form.errors
            status = 'yay! Merchant created'
            print "I work!"
            return render_to_response(template_name, {'form':form,'errors':errors,'status': status, 'merchant':request.merchant}, context_instance=RequestContext(request))
    else:
        form = MerchantForm(instance=request.merchant)
#        return render_to_response(template, context_instance=RequestContext(request, context))
        return render_to_response(template_name, {'form':form, 'status': status, 'merchant':request.merchant}, context_instance=RequestContext(request))
    


    
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
        
