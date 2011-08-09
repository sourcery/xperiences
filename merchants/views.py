from django.shortcuts import render_to_response
from django.template import RequestContext  # I still need to understand better the concept of RequestContext
#from experiences.models import Experience
#from merchants.models import Merchant
import pymongo

def merchant_profile(request, username):
    merchant = db.merchant.findOne({'username': username})
    
    template_name = 'merchants/merchant_profile.html'
    
    return render_to_response(template_name, {'merchant' : merchant}, context_instance=RequestContext(request))
# Create your views here.
