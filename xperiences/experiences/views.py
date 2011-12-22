from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from backend import configurations
from backend.decorators import merchant_required
from experiences.forms import ExperienceForm
from experiences.models import Experience, Category
import pymongo
from db_manage import db


def experience_by_category(request, category):
#    recent_experiences = Experience.objects.filter(category=category)

    template_name = 'experiences/index.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
    # or is that something that'll be determined by the urls.py?   I think this url should change!!

    return render_to_response(template_name, context_instance=RequestContext(request,{'category': category, 'categories':get_categories() }))


def experience_profile(request, id):
    experience = Experience.get_by_slug(id)

    #experience = wrapmongo(db.experience.find_one({'_id': pymongo.objectid.ObjectId(id)}))

    #merchant_tuple = experience["merchant"] # get a tuple with ObjectId and name

    #merchant_obj = wrapmongo(db.merchant.find_one({"_id": merchant_tuple[0]})) # get a merchant object

    merchant_obj = experience.merchant

    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?

    #more_experiences = wrapmongo(db.experience.find({'merchant': experience.get('merchant')}).limit(10))
    #more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]

    more_experiences = merchant_obj.experience_set.all()[:10]

    location ,address = experience.get_location_address()

    return render_to_response(template_name,
            {'experience': experience, 'merchant': merchant_obj, 'more_experiences': more_experiences ,'location' : location, 'address':address},
                              context_instance=RequestContext(request))


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


def index(request):
    #recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
    hits = request.session.get('hits', 0) + 1
    request.session['hits'] = hits

    # moved through the API
#    recent_experiences = Experience.objects.order_by("-pud_date")[:9]

    experience_of_the_day = get_experience_of_the_day()

    template_name = 'experiences/index.html'

    print "I am the index!"

    return render_to_response(template_name,
            {'hits': hits, 'eofd': experience_of_the_day, 'categories':get_categories()}, context_instance=RequestContext(request))

# test search
def search_experience(request):
    #recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
    hits = request.session.get('hits', 0) + 1
    request.session['hits'] = hits

    # moved through the API
    #    recent_experiences = Experience.objects.order_by("-pud_date")[:9]

    experience_of_the_day = get_experience_of_the_day()

    template_name = 'experiences/search.html'

    print "I am the index!"

    return render_to_response(template_name,
            {'hits': hits, 'eofd': experience_of_the_day, 'categories':get_categories()}, context_instance=RequestContext(request))

# how to extract active categories from Mongo to populate this list?
#active_categories = ['Adventure', 'Funky', 'save the world', 'Travel', 'Music', 'Skills']


def get_categories():
    return Category.get_all_categories()


def get_experience_of_the_day():
    try:
        Experience.objects.get(id=configurations.config['EXPERIENCE_OF_THE_DAY'])
    except Exception:
        return None

def add_experience_to_favorites(request):
    exp_id = request.POST['experience_id']  #({'_id':pymongo.objectid.ObjectId(id)}))
    #fav_experience = wrapmongo(db.experience.find_one({"_id": pymongo.objectid.ObjectId(exp_id)}))

    #get merchant
    merch_id = request.POST['merchant_id']
    fav_merchant = wrapmongo( db.merchant.find_one({"_id": pymongo.objectid.ObjectId(merch_id)}))

    #add experience id to favorite experiences in merchant collection
    if 'favorite_experiences' not in fav_merchant:
        fav_merchant["favorite_experience"] = []
    merchant_favorite_experiences = fav_merchant["favorite_experiences"]
    merchant_favorite_experiences.append(exp_id)
    db.merchant.save(fav_merchant)

    return HttpResponse("Favorite experience saved!")


def add_image(image, experience):
    """accepts image which is a django upload file object and an experience object.
        returns boolean for successful or not
    """
    filename = save_image(image)
    if 'images' in experience:
        experience['images'].append(filename)
    else:
        experience['images'] = [filename]
    db.experience.save(experience)
    return True


def add_image_to_experience(request, id):
    template_name = 'experiences/add_image.html'

    experience = Experience.objects.get(id=id)#db.experience.find_one({'_id': pymongo.objectid.ObjectId(id)})
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        image = request.FILES['image_1']
        add_image(image, experience)
        return HttpResponse("Your image was saved!")
    else:
        return render_to_response(template_name, {'experience': experience}, context_instance=RequestContext(request))


# need to read and learn about form validation... how to make sure that what people enter is valid... so many edge cases are possible...
@merchant_required()
def add_experience(request):
    status = ''
    if request.method == 'POST':
        data = request.POST
        if not len(data['title']):
            status = 'You must enter a title for the experience, otherwise how can people know how to find you?'
        elif len(data['title']) > 140:
            status = 'Title cannot be longer than 140 characters'
        else:
            pass
        if not len(data['description']):
            status = 'Please enter a description, so people can get a sense of the experience you are offering'
        if len(data['description']) > 2000:
            status = 'Please limit description to 2000 characters, to improve the chances that people will actually read it'
#        if 'category' not in data:
#            status = 'You must choose one category'
        if data['use_saved_address'] is True:
            pass    # here I should assign the merchant's address to the experience...
            # not sure how to do it b/c the experience is still not in created in mongo...
        elif not len(data['address']):  # are these supposed to be elif?
            status = 'Please enter a valid address'
#        elif len(data['city']) == 0:
#            status = 'Please enter city'
#        elif len(data['state']) == 0:
#            status = 'Please select state'
#        elif len(data['zipcode']) == 0:
#            status = 'Please enter zip-code'
#        elif data['country'] is None:
#            status = 'You must select a country'
#        else:
#            pass
        if not len(data['price']):
            status = 'Please enter price'
            #elif data['price'] is not a number:
            # status = 'Price must be a number'
            #elif data['price'] > 500000:
            # status = 'Price must be between $1 and $500,000. If you want to list a really expensive experience please contact us at support@tep.com'
        if len(request.FILES) > 0:
            data['merchant'] = request.merchant
#            experience = Experience(**data)
#            experience.update_location(float(request.POST.get('lat',0.0)), float(request.POST.get('lng',0.0)))
#            experience.save()
#            experience = create_experience(experience_collection, **data)
#            for k, v in request.FILES.iteritems():
#                add_image(v, experience)
        else:
            status = 'you must upload at least one image'

        new_object = Experience(merchant=request.merchant)
        form = ExperienceForm(request.POST,request.FILES,instance=new_object)
        if form.is_valid() and status == '':
            new_object = form.save()
            return redirect(reverse(experience_profile,kwargs = {'id':new_object.id}))
        else:
            return render_to_response('experiences/add_experience.html',context_instance=RequestContext(request, {'form':form, 'status':status}))
    else:
        form = ExperienceForm()
        return render_to_response('experiences/add_experience.html',context_instance=RequestContext(request, {'form':form}))


import random
import time
import settings
import os


def save_image(image):
    """accepts an image which is a django uploaded file object.
        returns a string filename, which is the path to where file is stored.
    """
    filename = os.path.join(settings.UPLOADED_IMAGES, random_name_generator())
    with open(filename, 'wb') as f:
        f.write(image.read())
    return filename


def random_name_generator():
    """does not accept anything.
        returns a randomly generated string.
    """
    return str(int(time.time())) + str(random.randint(10000, 999999))


def about(request):
    template_name = '/about.html'
    return render_to_response(template_name, context_instance=RequestContext(request))






#def index(request):
#    #recent_experiences = Experience.objects.get(pub_date=recent) # look into get function and SQL, Django ORM
#    hits = request.session.get('hits', 0) + 1
#    request.session['hits'] = hits
#
#    recent_experiences = Experience.objects.order_by("-pud_date")[9:18]
#
#    home_page_categories = get_categories()
#
#    experience_of_the_day = get_experience_of_the_day(db)
#
#    template_name = 'experiences/index.html'
#
#    print "I am the index!"
#
#    return render_to_response(template_name,
#            {'hits': hits, 'recent_experiences': recent_experiences, 'categories': home_page_categories,
#             'eofd': experience_of_the_day}, context_instance=RequestContext(request))
#

