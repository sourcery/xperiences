from django.shortcuts import render_to_response
from django.template import RequestContext  # I still need to understand better the concept of RequestContext
#from experiences.models import Experience
#from merchants.models import Merchant
import pymongo
from pymongo import objectid


def merchant_profile(request, username):
    merchant = wrapmongo(db.merchant.find_one({'username': username}))
    
    template_name = 'merchants/merchant_profile.html'
    
    return render_to_response(template_name, {'merchant' : merchant}, context_instance=RequestContext(request))


    
    
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
        




#def experience_profile(db, request, id):
#    #experience = Experience.objects.get(id=id) [django]
#
#    experience = wrapmongo(db.experience.find_one({'_id':pymongo.objectid.ObjectId(id)})) 
#    
#    merchant_tuple = experience["merchant"] # get a tuple with ObjectId and name
#    
#    merchant_obj = wrapmongo(db.merchant.find_one({"_id":merchant_tuple[0]})) # get a merchant object
#       
#    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?
#    
#    more_experiences = wrapmongo(db.experience.find({'merchant': experience.get('merchant', None)}).limit(10))
#    #more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]
#    
#    return render_to_response(template_name, {'experience': experience, 'merchant': merchant_obj, 'more_experiences': more_experiences}, context_instance=RequestContext(request))
