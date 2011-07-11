from django.db import models

from merchants.models import Merchant

class Experience(models.Model):
    title = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    location = models.CharField(max_length=100)
    #picture = models.ImageField(null=True) #null=True means that picture is not mandatory
    price = models.PositiveIntegerField(default=0)
    merchant = models.ForeignKey(Merchant)
    
    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
   