import datetime
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from backend.fields import  RichTextField, XPImageField, GeoModel, TextSearchModel, TextSearchField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals



class UserLog(models.Model):
    user = models.ForeignKey(User, null=True)
    session = models.CharField(max_length=100, null=True)
    was_logged_in = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime.datetime.now, editable=False)
    url = models.CharField(max_length=150)


    def __str__(self):
        return (str(self.user) if self.user else self.session) + ' ' + str(self.url)


    @staticmethod
    def create_from_user(user, url):
        return UserLog(user=user, was_logged_in=True, url=url)


    @staticmethod
    def create_from_session(session, url):
        return UserLog(session=session, url=url)


    @staticmethod
    def user_logged_in(user, session):
        logs = UserLog.objects.filter(session=session)
        for log in logs:
            log.user = user
            log.save()



class UserExtension(GeoModel,TextSearchModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True, null=True)
    validation_code = models.CharField(max_length=20, null=True, blank=True)
    is_merchant = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    credit = models.FloatField(default=0.0)
    FB_ID = models.CharField(max_length=40, null=True, blank=True)
    FB_token = models.CharField(max_length=255, null=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, related_name='referred_by')

    name = models.CharField(max_length=50)
    description = RichTextField(default='', blank=True)
    phone_number = models.CharField(max_length=15, default='', blank=True)
    website = models.CharField(max_length=100, default='', blank=True)

    bio = models.TextField(max_length=755,default='')
    birthday = models.DateField(null=True, blank=True)
    education = models.TextField(max_length=255, default='', blank=True)
    groups = models.TextField(max_length=755, default='', blank=True)
    user_events = models.TextField(max_length=755, default='', blank=True)
    hometown = models.TextField(max_length=255, default='', blank=True)
    user_interests = models.TextField(max_length=755, default='', blank=True)
    activities = models.TextField(max_length=755, default='', blank=True)
    friends = models.TextField(max_length=2500, default='', blank=True)
    photo = XPImageField(upload_to='photos_merchent',null=True,blank=True)

    offering = RichTextField(default='',blank=True)
    target_customers = RichTextField(default='',blank=True)



    class Meta:  # this is for the admin
        ordering = ['name']
        db_table = 'merchant'


    @staticmethod
    def get_merchant(**kwargs):
        try:
            kwargs['is_merchant'] = True
            return UserExtension.objects.get(**kwargs)
        except UserExtension.DoesNotExist:
            return None


    @staticmethod
    def create_merchant(**kwargs):
        kwargs['is_merchant'] = True
        obj = UserExtension(**kwargs)
        obj.save()
        return obj


    @staticmethod
    def create_from_user(user):
        ext = UserExtension(user=user, name=user.username)
        return ext


    def reward_credit(self, reward):
        self.credit += reward
        self.save()


    @property
    def slug(self):
        """accepts self and returns a string which is the slugified version of
            the instance's name.
        """
        return slugify(self.user.username)


    def __str__(self):
        return self.name


    def __unicode__(self):  # this is for the presentation in the admin site
        return self.name

class UserMessage(TextSearchModel):
    to = models.ForeignKey(UserExtension, related_name='merchant_user')
    sender = models.ForeignKey(UserExtension, related_name='sender_user', null=True,blank=True)
    sender_session = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(default=datetime.datetime.now,editable=False)
    title = TextSearchField(max_length=50,null=True,blank=True)
    message = TextSearchField(max_length=255,null=True,blank=True)

    def __str__(self):
        return str(self.title)


class SiteConfiguration(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    conf = models.TextField(max_length=1500, default='')


@receiver(signals.post_save, sender=User)
def user_post_save(instance, created, **_):
    pass
