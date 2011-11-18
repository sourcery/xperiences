from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db import models

from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

class Point(models.Model):
    latitude = models.FloatField()
    longtitude = models.FloatField()


class UserExtension(models.Model):
    user = models.ForeignKey(User)
    validation_code = models.CharField(max_length=20, default='', blank=True)
    is_merchant = models.BooleanField(default=False)
    good_points = models.IntegerField(default=0)
    FB_ID = models.CharField(max_length=40, default='', null=True)
    FB_token = models.CharField(max_length=120, default='', null=True)

    name = models.CharField(max_length=50, default='', blank=True)
    description = models.TextField(max_length=250, default='', blank=True)
    address = models.CharField(max_length=100, default='', blank=True)

    location = EmbeddedModelField(Point, null=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)

    birthday = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=255, default='', blank=True)
    groups = models.CharField(max_length=755, default='', blank=True)
    user_events = models.CharField(max_length=755, default='', blank=True)
    hometown = models.CharField(max_length=255, default='', blank=True)
    user_interests = models.CharField(max_length=755, default='', blank=True)
    activities = models.CharField(max_length=755, default='', blank=True)
    friends = models.CharField(max_length=5000, default='', blank=True)

    objects = MongoDBManager()

    @staticmethod
    def create_from_user(user):
        ext = UserExtension(user=user, name=user.username)
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
