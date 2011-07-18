from django.db import models

from merchants.models import Merchant

class Experience(models.Model):
    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    #picture = models.ImageField(null=True) #null=True means that picture is not mandatory
    price = models.PositiveIntegerField(default=0)
    merchant = models.ForeignKey(Merchant)
    pub_date = models.DateField()

    
    def slug(self):
        """accepts self and returns a string which is the slugified version of
            the instance's name.
        """
        return slugify(self.title)
    
    
    active_categories = ['adventure', 'food', 'save the world', 'romance', 'music', 'education']
    
    
    
    
    
    
    class Meta:  # what is this class Meta?
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
   