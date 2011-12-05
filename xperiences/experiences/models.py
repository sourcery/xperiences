import datetime
from backend import configurations
from backend.models import GeoModel, UserExtension, RichTextField
from django.db import models
from django.template.defaultfilters import slugify
from sorl.thumbnail import ImageField


#from merchants.models import Merchant
choices = configurations.get_categories()

class Experience(GeoModel):
    merchant = models.ForeignKey(UserExtension,null=True)

    is_active = models.BooleanField(default=True)

    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = RichTextField()
    category = models.CharField(max_length=50, choices=choices)
    price = models.PositiveIntegerField(default=0)
    unit_name = models.CharField(max_length=100) # eg.: week, meal, day...
    unit_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    pub_date = models.DateField(default=datetime.date.today,null=True)
    photo1 = ImageField(upload_to='%Y%m%d%H%M%S',null=True,blank=True)
    photo2 = ImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo3 = ImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo4 = ImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo5 = ImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    video_link = models.TextField(max_length=150,null=True,blank=True)
    use_saved_address = models.BooleanField(default=True)

    valid_from = models.DateTimeField(default=datetime.datetime.now)
    valid_until = models.DateTimeField(null=True,blank=True)
    tags = models.CharField(max_length=100,default='')

    my_place = models.BooleanField(default=False,verbose_name='Hosting at my place')
    delivery = models.BooleanField(default=False,verbose_name='Delivery')
    pick_up = models.BooleanField(default=False,verbose_name='Pick up')
    capacity = models.CharField(max_length=7,default='1-5',choices=[('1-5','1-5'),('6-10','6-10'),('11-15','11-15'),('16-20','16-20'),('20+','More than 20'),('+','until I\'ll ran out of food')])


    def get_location_address(self):
        if self.use_saved_address:
            return self.merchant.xp_location , self.merchant.address
        else:
            return self.xp_location, self.address


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
