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
