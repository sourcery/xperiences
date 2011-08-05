from django.shortcuts import render_to_response  # renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text
from django.template import RequestContext
from experiences.models import Experience

def experience_by_category(request, category):
    #experiences = Experience.objects.all()
    
    experiences = db.experience.find({'category':category})
    
    template_name = 'experiences/list_experiences.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
                                                         # or is that something that'll be determined by the urls.py?   
    
    return render_to_response(template_name, {'experiences' : experiences}, context_instance=RequestContext(request))


def experience_profile(request, id):
    #experience = Experience.objects.get(id=id) [django]
    
    experience = db.experience.findOne({'_id':ObjectId(id)})

    
    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?
    
    more_experiences = db.experience.find({'merchant':experience['merchant']}).limit(5)
    more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]
    
    return render_to_response(template_name, {'experience': experience, 'more_experiences': more_experiences}, context_instance=RequestContext(request))
    
    


def index(request):
    #recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
    
    recent_experiences = db.experience.find().sort(['-pub_date']).limit(9)
       
    home_page_categories = get_categories()
    
    experience_of_the_day = get_experience_of_the_day()

    template_name = 'experiences/index.html'
    
    return render_to_response(template_name, {'recent_experiences': recent_experiences, 'categories': home_page_categories, 'eofd': experience_of_the_day}, context_instance=RequestContext(request))


active_categories = ['adventure', 'food', 'save the world', 'romance', 'music', 'education']


def get_categories():
    return active_categories    



def get_experience_of_the_day():
    experience_of_the_day = db.experience.findOne({'_id':ObjectId("4e3722fcd01724fa2a0c0017")}) # every day I can change the ID of the experience based on the experience of the day.
    return experience_of_the_day



