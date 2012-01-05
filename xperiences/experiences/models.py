import datetime
from backend.fields import GeoModel, RichTextField, XPImageField, TextSearchField, TextSearchModel
from backend.models import UserExtension
from django.db import models
from django.template.defaultfilters import slugify


#from merchants.models import Merchant
cached_categories = None
class Category(models.Model):
    slug = models.CharField(max_length=30)
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_all_categories():
        global cached_categories
        if not cached_categories:
            cached_categories = Category.objects.all()
        return cached_categories

    def save(self, *args, **kwargs):
        global cached_categories
        cached_categories = None
        return super(Category,self).save(*args,**kwargs)


class Experience(GeoModel):
    use_saved_address = models.BooleanField(default=True,verbose_name='Use merchant address (if clicked,address above will be ignored)')
    merchant = models.ForeignKey(UserExtension,null=True)

    is_active = models.BooleanField(default=True)

    title = TextSearchField(max_length=50,unique=True)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    slug_id = models.CharField(max_length=50,editable=False)
    description = RichTextField()
    category = models.ForeignKey(Category,null=True)
    price = models.PositiveIntegerField(default=0)
    unit_name = models.CharField(max_length=100, null=True, blank=True) # eg.: week, meal, day...
    unit_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    pub_date = models.DateField(default=datetime.date.today,null=True)
    photo1 = XPImageField(upload_to='%Y%m%d%H%M%S')
    photo2 = XPImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo3 = XPImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo4 = XPImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    photo5 = XPImageField(upload_to='%Y%m%d%H%M%S', null=True, blank=True)
    video_link = models.CharField(max_length=150,null=True,blank=True) #TextField makes it be a text area which is not what we want

    #date = models.DateField()
    #time = models.TimeField()
    valid_from = models.DateTimeField(default=datetime.datetime.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    tags = models.CharField(max_length=100, default='', null=True, blank=True)

    my_place = models.BooleanField(default=False,verbose_name='Hosting at my place')
    delivery = models.BooleanField(default=False,verbose_name='Delivery')
    pick_up = models.BooleanField(default=False,verbose_name='Pick up')
    capacity = models.CharField(max_length=7,default='1-5',choices=[('1-5','1-5'),('6-10','6-10'),('11-15','11-15'),('16-20','16-20'),('20+','More than 20'),('+','until I run out of food')])


    #capacity = models.CharField(max_length=7,default='1-5',choices=[('1-5','1-5'),('6-10','6-10'),('11-15','11-15'),('16-20','16-20'),('20+','More than 20'),('+','until I run out of food')])


    def get_location_address(self):
        if self.use_saved_address:
            return self.merchant.xp_location , self.merchant.address
        else:
            return self.xp_location, self.address

    @staticmethod
    def get_by_slug(slug_id):
        return Experience.objects.get(slug_id=slug_id)

    def save(self, *args, **kwargs):
        if self.use_saved_address:
            self.xp_location = self.merchant.xp_location
            self.address = self.merchant.address
        self.slug_id = self.slug
        return super(Experience,self).save(self,*args,**kwargs)


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
