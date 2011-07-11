from django.db import models
from django.db.models.signals import pre_save  # UB
from django.template.defaultfilters import slugify  # UB

class Merchant(models.Model):
    name = models.CharField(max_length=50)  # by default blank=false and null=false, meaning that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    slug = models.SlugField(max_length=50, db_index=True, blank=True)  # UB
    
    class Meta:   # UB
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
    
    
def pre_save_merchant(sender, instance, **kwargs):
    
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_merchant, sender=Merchant)


# more things related to merchant:
#- email / pw
#- credit card number / paypal for paying fees
#- bank account and routing for sending payments
#- probably some IRS stuff like EIN