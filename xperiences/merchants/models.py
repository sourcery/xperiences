from django.db import models
from django.contrib.localflavor.us.models import *
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

class Merchant(models.Model):

    # username
    name = models.CharField(max_length=50)  # by default blank=false and null=false, means that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField()
    #zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=75)
    photo = models.FileField(upload_to='photos_merchent')
    
    @property
    def slug(self):
        """accepts self and returns a string which is the slugified version of
            the instance's name.
        """
        return slugify(self.name)

    # Give your model metadata by using inner class Meta. Model metadata is anything that's not a field, such as
    # ordering options, db table names or human readable names. So this meta class orders the Merchant class
    # by 'name' in the admin interface.
    class Meta:
        ordering = ['name'] # This is a list that specifies the ordering
        db_table = 'merchant'

    def __unicode__(self):  # this is for the presentation in the admin site
        return self.name

# Django includes a "signal dispatcher" which helps allow decoupled applications get notified when actions occur elsewhere
# in the framework. To receive a signal, you need to register a receiver function that gets called when the signal is sent by
# using the Signal.connect() method:

# Here we define a receiver function (a receiver can be any Python function or method). The purpose is to slugify merchant based on the Merchant's name.
#def pre_save_merchant(sender, instance, **kwargs):
#
#    if not instance.slug:
#        instance.slug = slugify(instance.name)
#
## this is the Signal.connect() method calling the receiver function.
#pre_save.connect(pre_save_merchant, sender=Merchant)  # sender=Merchant means that we only receive signals sent from the Merchant model.
#


# more things related to merchant:
#- email / pw
#- credit card number / paypal for paying fees
#- bank account and routing for sending payments
#- probably some IRS stuff like EIN


#slug = models.SlugField(max_length=50, db_index=True, blank=True)  # you can use the slug to identify the merchant (rather than ID)
