from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from backend.models import UserExtension
from django.shortcuts import render_to_response
from django.template import RequestContext  # I still need to understand better the concept of RequestContext
#from experiences.models import Experience
#from merchants.models import Merchant


def merchant_profile(request, username):
    merchant = UserExtension.get_merchant(user=User.objects.get(username=username))
    template_name = 'merchants/merchant_profile.html'
    return render_to_response(template_name, {'merchant': merchant}, context_instance=RequestContext(request))


@login_required()
def register(request):
    status = ''
    template_name = 'merchants/register.html'
    if request.method == 'POST':
        data = request.POST
        merchant = request.merchant
        for key in data:
            if hasattr(merchant,key):
                setattr(merchant,key,data[key])
        merchant.save()
        status = 'yay! Merchant created'
        print "I work!"
        return render_to_response(template_name, {'status': status, 'merchant':merchant}, context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, {'status': status, 'merchant':request.merchant}, context_instance=RequestContext(request))
    


    
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
        
