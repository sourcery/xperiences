<<<<<<< HEAD
from backend.models import GeoModel, UserExtension
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

#from merchants.models import Merchant

class Experience(GeoModel):
    merchant = models.ForeignKey(UserExtension,null=True)
    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    #picture = models.ImageField(upload_to="/uploads", null=True) #null=True means that picture is not mandatory
    price = models.PositiveIntegerField(default=0)
#    merchant = models.ForeignKey(Merchant, null=True)
    pub_date = models.DateField(null=True)
    photos = models.FileField(upload_to='photos')
    photo2 = models.ImageField(upload_to='photos',null=True,blank=True)
    photo3 = models.ImageField(upload_to='photos',null=True,blank=True)
    photo4 = models.ImageField(upload_to='photos',null=True,blank=True)
    photo5 = models.ImageField(upload_to='photos',null=True,blank=True)
=======
from django.db import models
from django.template.defaultfilters import slugify

from merchants.models import Merchant

class Experience(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    merchant = models.ForeignKey(Merchant, null=True)
    pub_date = models.DateField(null=True)
    photo1 = models.FileField(upload_to='%Y%m%d%H%M%S')
    photo2 = models.FileField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo3 = models.FileField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo4 = models.FileField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo5 = models.FileField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
>>>>>>> 8a9cdb4e5e2e52acc7bfcf12e4b06840a559f59a


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
