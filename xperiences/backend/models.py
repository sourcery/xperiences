import datetime
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.forms.fields import CharField
from django.template.defaultfilters import slugify
from backend.forms import PointWidgetWithAddressField, RichTextEditorWidget
from django_mongodb_engine.contrib import MongoDBManager

__author__ = 'ishai'

from django.db import models
from djangotoolbox.fields import EmbeddedModelField




class Coordinate(models.Model):
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    geom_type = 'POINT'

    def __str__(self):
        return '%f,%f' % (self.lat, self.lng)




class GeoField(EmbeddedModelField):
    address_field = ''
    def __init__(self,**kwargs):
        kwargs['default'] = Coordinate
#        kwargs['editable'] = False
        if 'address_field' in kwargs:
            self.address_field = 'id_' + kwargs.get('address_field','')
            del kwargs['address_field']
        return super(GeoField,self).__init__(Coordinate, **kwargs)

    def formfield(self, **kwargs):
            # A file widget is provided, but use model FileField or ImageField
        # for storing specific files most of the time
        defaults = {'widget': PointWidgetWithAddressField(self.address_field)}
#        attrs = kwargs.get('attrs',{})
#        attrs['address_field'] = self.address_field
        defaults.update(kwargs)
#        defaults['attrs'] = attrs
        return super(GeoField, self).formfield(self.FormClass,**defaults)

    class FormClass(CharField):
        def to_python(self, (lat,lng)):
            return Coordinate(lat=lat, lng=lng)

class RichTextField(models.TextField):
    def __init__(self,**kwargs):
        defaults = {'max_length':255}
        defaults.update(kwargs)
        return super(RichTextField,self).__init__(**defaults)

    def formfield(self,**kwargs):
        kwargs['widget'] = RichTextEditorWidget
        return super(RichTextField,self).formfield(**kwargs)

class XPDBManager(MongoDBManager):
    def proximity_query(self,location,**kwargs):
        max_distance = kwargs.get('max_distance',10)
        field_name = kwargs.get('field','xp_location')
        lat = location['lat']
        lng = location['lng']
        query = kwargs.get('query',{})
        query[field_name] = {'$near' : { 'lat' : lat, 'lng':lng} }
        return self.raw_query(query)


class GeoModel(models.Model):

    xp_location = GeoField(address_field='address')
    address = models.CharField(max_length=100, default='',blank=True)

    objects = XPDBManager()

    def update_location(self,lat,lng):
        self.xp_location.lat = lat
        self.xp_location.lng = lng

    class Meta:
        abstract = True

class UserLog(models.Model):
    user = models.ForeignKey(User, null=True)
    session = models.CharField(max_length=100,null=True)
    was_logged_in = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime.datetime.now, editable=False)
    url = models.CharField(max_length=150)

    def __str__(self):
        return (str(self.user) if self.user else self.session) + ' ' + str(self.url)


    @staticmethod
    def create_from_user(user,url):
        return UserLog(user=user,was_logged_in=True,url=url)

    @staticmethod
    def create_from_session(session,url):
        return UserLog(session=session,url=url)

    @staticmethod
    def user_logged_in(user,session):
        logs = UserLog.objects.filter(session=session)
        for log in logs:
            log.user = user
            log.save()

class UserExtension(GeoModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True,primary_key=True)
    validation_code = models.CharField(max_length=20, null=True,blank=True)
    is_merchant = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    credit = models.FloatField(default=0.0)
    FB_ID = models.CharField(max_length=40, null=True,blank=True)
    FB_token = models.CharField(max_length=255,null=True,blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, related_name='referred_by')

    name = models.CharField(max_length=50)  # by default blank=false and null=false, means that both fields are mandatory in both admin and DB
    description = RichTextField(default='',blank=True)
    phone_number = models.CharField(max_length=15, default='',blank=True)
    website = models.CharField(max_length=100, default='',blank=True)

    birthday = models.DateField(null=True,blank=True)
    education = models.TextField(max_length=255,default='',blank=True)
    groups = models.TextField(max_length=755,default='',blank=True)
    user_events = models.TextField(max_length=755,default='',blank=True)
    hometown = models.TextField(max_length=255,default='',blank=True)
    user_interests = models.TextField(max_length=755,default='',blank=True)
    activities = models.TextField(max_length=755,default='',blank=True)
    friends = models.TextField(max_length=2500,default='',blank=True)
    photo = models.FileField(upload_to='photos_merchent',null=True,blank=True)


    @staticmethod
    def get_merchant(**kwargs):
        try:
            kwargs['is_merchant'] = True
            return UserExtension.objects.get(**kwargs)
        except UserExtension.DoesNotExist:
            return None

    @staticmethod
    def create_merchant(**kwargs):
        kwargs['is_merchant'] = True
        obj = UserExtension(**kwargs)
        obj.save()
        return obj

    @staticmethod
    def create_from_user(user):
        ext = UserExtension(user=user, name=user.username )
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

#class Listing(GeoModel):
#    user = models.ForeignKey(User)
#    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
#    description = models.TextField(max_length=250)
#    category = models.CharField(max_length=50)
#    address = models.CharField(max_length=100)
#    #picture = models.ImageField(upload_to="/uploads", null=True) #null=True means that picture is not mandatory
#    price = models.FloatField(default=0.0)
#    pub_date = models.DateField(null=True)
#    photos = models.FileField(upload_to='photos')
#    photo2 = models.FileField(upload_to='photos',null=True,blank=True)
#    photo3 = models.FileField(upload_to='photos',null=True,blank=True)
#    photo4 = models.FileField(upload_to='photos',null=True,blank=True)
#    photo5 = models.FileField(upload_to='photos',null=True,blank=True)
#
#
#    @property
#    def slug(self):
#        """accepts self and returns a string which is the slugified version of
#            the instance's name.
#        """
#        return slugify(self.title)
#
#
#
#    class Meta:  # this is for the admin
#        ordering = ['title']
#        db_table = 'experience'
#
#    def __unicode__(self):
#        return self.title

class SiteConfiguration(models.Model):
    name = models.CharField(max_length=50,primary_key=True)
    conf = models.TextField(max_length=1500,default='')


from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher

@receiver(signals.post_save, sender=User)
def user_post_save(instance, created, **_):
    pass
#    session = _['request'].session.session_key
#    UserLog.user_logged_in(instance,session)


