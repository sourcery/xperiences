from django.shortcuts import render_to_response  # renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text
from django.template import RequestContext
from django.http import HttpResponse
<<<<<<< HEAD
from backend import configurations
=======
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a
from experiences.models import Experience
import pymongo
from db_manage import db


def experience_by_category(request, category):
    #experiences = Experience.objects.all()

<<<<<<< HEAD
    experiences = Experience.objects.filter(category=category)

    template_name = 'experiences/list_experiences.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
    # or is that something that'll be determined by the urls.py?   I think this url should change!!

    return render_to_response(template_name, {'experiences': experiences}, context_instance=RequestContext(request))
=======
    recent_experiences = Experience.objects.filter(category=category).order_by("-pud_date")

    template_name = 'experiences/index.html'  # aren't we supposed to have something like experiences/category/list_experiences.html?
    # or is that something that'll be determined by the urls.py?   I think this url should change!!

    return render_to_response(template_name, {'recent_experiences': recent_experiences, 'category': category}, context_instance=RequestContext(request))
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a


def experience_profile(request, id):
    experience = Experience.objects.get(id=id) 

<<<<<<< HEAD
    experience = wrapmongo(Experience.objects.get(id=pymongo.objectid.ObjectId(id)))  # db.experience.find_one({'_id': pymongo.objectid.ObjectId(id)}))

    merchant_tuple = experience['merchant'] # get a tuple with ObjectId and name

    merchant_obj = wrapmongo(db.merchant.find_one({"_id": merchant_tuple[0]})) # get a merchant object

    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?

    more_experiences = wrapmongo(db.experience.find({'merchant': experience.get('merchant')}).limit(10))
    #more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]
=======
    #experience = wrapmongo(db.experience.find_one({'_id': pymongo.objectid.ObjectId(id)}))

    #merchant_tuple = experience["merchant"] # get a tuple with ObjectId and name

    #merchant_obj = wrapmongo(db.merchant.find_one({"_id": merchant_tuple[0]})) # get a merchant object
    
    merchant_obj = experience.merchant

    template_name = 'experiences/experience_profile.html' # should we slugify the name of experience?

    #more_experiences = wrapmongo(db.experience.find({'merchant': experience.get('merchant')}).limit(10))
    #more_experiences = [e for e in more_experiences if e['_id'] != experience['_id']]
    
    more_experiences = merchant_obj.experience_set.all()[:10]
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a

    return render_to_response(template_name,
            {'experience': experience, 'merchant': merchant_obj, 'more_experiences': more_experiences},
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

<<<<<<< HEAD
    recent_experiences = Experience.objects.order_by("-pud_date")[:9]

    home_page_categories = get_categories()

    experience_of_the_day = get_experience_of_the_day()
=======
    recent_experiences = Experience.objects.order_by("-pud_date")[9:18]

    home_page_categories = get_categories()

    experience_of_the_day = get_experience_of_the_day(db)
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a

    template_name = 'experiences/index.html'

    print "I am the index!"

    return render_to_response(template_name,
            {'hits': hits, 'recent_experiences': recent_experiences, 'categories': home_page_categories,
             'eofd': experience_of_the_day}, context_instance=RequestContext(request))


# how to extract active categories from Mongo to populate this list?
active_categories = ['Adventure', 'Funky', 'save the world', 'Travel', 'Music', 'Skills']


def get_categories():
    return active_categories


<<<<<<< HEAD
def get_experience_of_the_day():
    try:
        Experience.objects.get(id=configurations.config['EXPERIENCE_OF_THE_DAY'])
    except Experience.DoesNotExist:
        return None
=======
def get_experience_of_the_day(db):
    experience_of_the_day = db.experience.find_one({'_id': pymongo.objectid.ObjectId(
        "4e3722fcd01724fa2a0c0017")}) # every day I can change the ID of the experience based on the experience of the day.
    return experience_of_the_day

>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a

def add_experience_to_favorites(request):
    exp_id = request.POST['experience_id']  #({'_id':pymongo.objectid.ObjectId(id)}))
    #fav_experience = wrapmongo(db.experience.find_one({"_id": pymongo.objectid.ObjectId(exp_id)}))

    #get merchant
    merch_id = request.POST['merchant_id']
    fav_merchant = wrapmongo(db.merchant.find_one({"_id": pymongo.objectid.ObjectId(merch_id)}))

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
    experience = db.experience.find_one({'_id': pymongo.objectid.ObjectId(id)})
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        image = request.FILES['image_1']
        add_image(image, experience)
        return HttpResponse("Your image was saved!")
    else:
        return render_to_response(template_name, {'experience': experience}, context_instance=RequestContext(request))


# need to read and learn about form validation... how to make sure that what people enter is valid... so many edge cases are possible...
def add_experience(request):
    status = ''
    if request.method == 'POST':
        data = request.POST
        if len(data['title']) == 0:
            status = 'You must enter a title for the experience, otherwise how can people know how to find you?'
        elif len(data['title']) > 140:
            status = 'Title cannot be longer than 140 characters'
        else:
            pass
        if len(data['description']) == 0:
            status = 'Please enter a description, so people can get a sense of the experience you are offering'
        if len(data['description']) > 2000:
            status = 'Please limit description to 2000 characters, to improve the chances that people will actually read it'
        else:
            pass
        if data['category'] is None:
            status = 'You must choose one category'
        else:
            pass
        if data['use_my_address'] is True:
            pass    # here I should assign the merchant's address to the experience...
            # not sure how to do it b/c the experience is still not in created in mongo...
        elif len(data['address']) == 0:  # are these supposed to be elif?
            status = 'Please enter a valid address'
        elif len(data['city']) == 0:
            status = 'Please enter city'
        elif len(data['state']) == 0:
            status = 'Please select state'
        elif len(data['zipcode']) == 0:
            status = 'Please enter zip-code'
        elif data['country'] is None:
            status = 'You must select a country'
        else:
            pass
        if len(data['price']) == 0:
            status = 'Please enter price'
            #elif data['price'] is not a number:
            # status = 'Price must be a number'
            #elif data['price'] > 500000:
            # status = 'Price must be between $1 and $500,000. If you want to list a really expensive experience please contact us at support@tep.com'
        if len(request.FILES) > 0:
            experience = create_experience(experience_collection, **data)
            for k, v in request.FILES.iteritems():
                add_image(v, experience)
            status = 'yay! experience created'
        else:
            status = 'you must upload at least one image'


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











