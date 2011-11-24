from backend.models import UserExtension
from django.shortcuts import render_to_response
from django.template import RequestContext  # I still need to understand better the concept of RequestContext
#from experiences.models import Experience
#from merchants.models import Merchant


def merchant_profile(request, username):
    merchant = UserExtension.get_merchant(username=username)
    template_name = 'merchants/merchant_profile.html'
    return render_to_response(template_name, {'merchant': merchant}, context_instance=RequestContext(request))

    
def register(request):
    status = ''
    if request.method == 'POST':
        data = request.POST
        if len(data['email']) == 0:
            status = 'please enter your email'
        else:
            pass
        if UserExtension.get_merchant(email=data['email']) is not None:
            status = 'a user already exists for this email. Try again'
        else:
            UserExtension.create_merchant(**data)
#            create_merchant(merchant_collection, **data)
            status = 'yay! Merchant created'
            
    else: 
        pass
    
    template_name = 'merchants/register.html'
    print "I work!"
    return render_to_response(template_name, {'status': status}, context_instance=RequestContext(request))


    
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
        
