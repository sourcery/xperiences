from django.shortcuts import render_to_response  # renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text
from django.template import RequestContext
from experiences.models import Experience

def experience_by_category(request):
    experiences = Experience.objects.all()
    
    template_name = 'experiences/list_experiences.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
                                                         # or is that something that'll be determined by the urls.py?   
    
    return render_to_response(template_name, {'experiences' : experiences}, context_instance=RequestContext(request))


def experience_profile(request, id):
    experience = Experience.objects.get(id=id)
    
    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?
    
    # TO DO - add featuers later
    more_experiences = []
    
    return render_to_response(template_name, {'experience': experience, 'more_experiences': more_experiences}, context_instance=RequestContext(request))
    
    


def index(request):
    recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
        
    home_page_categories = get_categories()
    
    experience_of_the_day = get_experience_of_the_day()

    template_name = 'experiences/index.html'
    
    return render_to_response(template_name, {'recent_experiences': recent_experiences, 'categories': home_page_categories, 'eofd': experience_of_the_day}, context_instance=RequestContext(request))


"""
def get_categories():
    return Experience.active_categories    
"""

"""
def get_experience_of_the_day():
    experience_of_the_day = Experience.objects.get(id=#) # every day I can change the ID of the experience based on the experience of the day.
    return experience_of_the_day

"""

