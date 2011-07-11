from django.shortcuts import render_to_response
from django.template import RequestContext
from experiences.models import Experience

def index(request):
    experiences = Experience.objects.all()
    
    template_name = 'experiences/list_experiences.html'
    
    return render_to_response(template_name, {'experiences' : experiences}, context_instance=RequestContext(request))


def view_experience_profile(request, id):
    experience = Experience.objects.get(id=id)
    
    template_name = 'experiences/experience_profile.html'
    
    return render_to_response(template_name, {'experience' : experience}, context_instance=RequestContext(request))
