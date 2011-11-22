from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_mongodb_engine.contrib import MongoDBManager

__author__ = 'ishai'

from django.db import models
from djangotoolbox.fields import EmbeddedModelField

class Coordinate(models.Model):
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

class GeoField(EmbeddedModelField):
    def __init__(self):
        super(GeoField,self).__init__(Coordinate)

class XPDBManager(MongoDBManager):
    def proximity_query(self,location,**kwargs):
        max_distance = kwargs.get('max_distance',10)
        field_name = kwargs.get('field','xp_location')
        lat = location['lat']
        lng = location['lng']
        return self.raw_query({field_name : {'$near' : { 'lat' : lat, 'lng':lng},'$maxDistance' : max_distance }})


class GeoModel(models.Model):

    xp_location = GeoField()

    objects = XPDBManager()

    def update_location(self,lat,lng):
        self.xp_location.lat = lat
        self.xp_location.lng = lng

    class Meta:
        abstract = True


class UserExtension(GeoModel):
    user = models.ForeignKey(User, unique=True,primary_key=True)
    validation_code = models.CharField(max_length=20)
    is_merchant = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    credit = models.FloatField(default=0.0)
    FB_ID = models.CharField(max_length=40, null=True)
    FB_token = models.CharField(max_length=40,null=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, related_name='referred_by')

    name = models.CharField(max_length=50)  # by default blank=false and null=false, means that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250, default='')
    address = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=15, default='')
    website = models.CharField(max_length=100, default='')

    birthday = models.DateField(null=True,blank=True)
    education = models.TextField(max_length=255,default='')
    groups = models.TextField(max_length=755,default='')
    user_events = models.TextField(max_length=755,default='')
    hometown = models.TextField(max_length=255,default='')
    user_interests = models.TextField(max_length=755,default='')
    activities = models.TextField(max_length=755,default='')
    friends = models.TextField(max_length=2500,default='',blank='')
    photo = models.ImageField(upload_to='photos_merchent')

    @staticmethod
    def create_from_user(user):
        ext = UserExtension(user=user,name=user.username )
        return ext

    def reward_credit(self,reward):
        self.credit += reward
        self.save()

    @property
    def slug(self):
        """accepts self and returns a string which is the slugified version of
            the instance's name.
        """
        return slugify(self.user.username)

    # Give your model metadata by using inner class Meta. Model metadata is anything that's not a field, such as
    # ordering options, db table names or human readable names. So this meta class orders the Merchant class
    # by 'name' in the admin interface.
    class Meta:
        ordering = ['name'] # This is a list that specifies the ordering

    def __str__(self):
        return self.name

    def __unicode__(self):  # this is for the presentation in the admin site
        return self.name

class Listing(GeoModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    #picture = models.ImageField(upload_to="/uploads", null=True) #null=True means that picture is not mandatory
    price = models.FloatField(default=0.0)
    pub_date = models.DateField(null=True)
    photos = models.ImageField(upload_to='photos')
    photo2 = models.ImageField(upload_to='photos')
    photo3 = models.ImageField(upload_to='photos')
    photo4 = models.ImageField(upload_to='photos')
    photo5 = models.ImageField(upload_to='photos')


    @property
    def slug(self):
        """accepts self and returns a string which is the slugified version of
            the instance's name.
        """
        return slugify(self.title)



    class Meta:  # this is for the admin
        ordering = ['title']
        db_table = 'experience'

    def __unicode__(self):
        return self.title
