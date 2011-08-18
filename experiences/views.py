from django.shortcuts import render_to_response  # renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text
from django.template import RequestContext
#from experiences.models import Experience
import pymongo
from pymongo import objectid
import functions

def experience_by_category(db, request, category):
    #experiences = Experience.objects.all()
    
    experiences = db.experience.find({'category':category})
    
    template_name = 'experiences/list_experiences.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
                                                         # or is that something that'll be determined by the urls.py?   I think this url should change!!
    
    return render_to_response(template_name, {'experiences' : experiences}, context_instance=RequestContext(request))


def experience_profile(db, request, id):
    #experience = Experience.objects.get(id=id) [django]

    experience = wrapmongo(db.experience.find_one({'_id':pymongo.objectid.ObjectId(id)})) 
    
    merchant_tuple = experience["merchant"] # get a tuple with ObjectId and name
    
    merchant_obj = wrapmongo(db.merchant.find_one({"_id":merchant_tuple[0]})) # get a merchant object
       
    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?
    
    more_experiences = wrapmongo(db.experience.find({'merchant': experience.get('merchant', None)}).limit(10))
    #more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]
    
    return render_to_response(template_name, {'experience': experience, 'merchant': merchant_obj, 'more_experiences': more_experiences}, context_instance=RequestContext(request))
    
    
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
        
def index(db, request):
    #recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
    
    recent_experiences = wrapmongo(db.experience.find(sort=[('pub_date', -1)], limit=9))
       
    home_page_categories = get_categories()
    
    experience_of_the_day = get_experience_of_the_day(db)

    template_name = 'experiences/index.html'
    
    return render_to_response(template_name, {'recent_experiences': recent_experiences, 'categories': home_page_categories, 'eofd': experience_of_the_day}, context_instance=RequestContext(request))


# how to extract active categories from Mongo to populate this list?
active_categories = ['Adventure', 'Funky', 'save the world', 'Travel', 'Music', 'Skills']


def get_categories():
    return active_categories    



def get_experience_of_the_day(db):
    experience_of_the_day = db.experience.find_one({'_id':pymongo.objectid.ObjectId("4e3722fcd01724fa2a0c0017")}) # every day I can change the ID of the experience based on the experience of the day.
    return experience_of_the_day



