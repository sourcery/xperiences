from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

__author__ = 'ishai'

from django.db import models

class UserExtension(models.Model):
    user = models.ForeignKey(User)
    validation_code = models.CharField(max_length=20)
    is_merchant = models.BooleanField(default=False)
    good_points = models.IntegerField(default=0)
    FB_ID = models.CharField(max_length=40, null=True)
    FB_token = models.CharField(max_length=40,null=True)

    name = models.CharField(max_length=50)  # by default blank=false and null=false, means that both fields are mandatory in both admin and DB
    description = models.TextField(max_length=250)
    address = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    phone_number = models.CharField(max_length=15)
    website = models.CharField(max_length=100)

    @staticmethod
    def create_from_user(user):
        ext = UserExtension(user=user,name=user.username )
        return ext

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

    def __unicode__(self):  # this is for the presentation in the admin site
        return self.name
