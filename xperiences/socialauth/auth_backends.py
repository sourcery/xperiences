from backend.models import UserExtension, UserLog
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
import facebook

import urllib
from socialauth.lib import oauthtwitter2 as oauthtwitter
from socialauth.models import OpenidProfile as UserAssociation, TwitterUserProfile, FacebookUserProfile, LinkedInUserProfile, AuthMeta
from socialauth.lib.linkedin import *
import traceback

import random
import datetime
import cgi
from backend import utils

TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

# Linkedin
LINKEDIN_CONSUMER_KEY = getattr(settings, 'LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET = getattr(settings, 'LINKEDIN_CONSUMER_SECRET', '')

# OpenId setting map

OPENID_AX_PROVIDER_MAP = getattr(settings, 'OPENID_AX_PROVIDER_MAP', {})

class OpenIdBackend:
    def authenticate(self, openid_key, request, provider, user=None):
        try:
            print 'authenticating by openid_key'
            assoc = UserAssociation.objects.get(openid_key = openid_key)
            u = assoc.user
            print u.id
            return u
        except UserAssociation.DoesNotExist:
            print 'user is not signed'
            #fetch if openid provider provides any simple registration fields
            nickname = None
            email = None
            firstname = None
            lastname = None
            
            if request.openid and request.openid.sreg:
                email = request.openid.sreg.get('email')
                nickname = request.openid.sreg.get('nickname')
                firstname, lastname = request.openid.sreg.get('fullname', ' ').split(' ', 1)
            elif request.openid and request.openid.ax:
                email = request.openid.ax.getSingle('http://axschema.org/contact/email')
                if 'google' in provider:
                    ax_schema = OPENID_AX_PROVIDER_MAP['Google']
                    firstname = request.openid.ax.getSingle(ax_schema['firstname'])
                    lastname = request.openid.ax.getSingle(ax_schema['lastname'])
                    nickname = email.split('@')[0]
                else:
                    ax_schema = OPENID_AX_PROVIDER_MAP['Default']
                    try:
                        nickname = request.openid.ax.getSingle(ax_schema['nickname']) #should be replaced by correct schema
                        firstname, lastname = request.openid.ax.getSingle(ax_schema['fullname']).split(' ', 1)
                    except:
                        pass

            if nickname is None :
                nickname =  ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(10)])
            
            name_count = User.objects.filter(username__startswith = nickname).count()
            if name_count:
                username = '%s%d' % (nickname, name_count + 1)
            else:
                username = '%s' % (nickname)
                
            if email is None :
                valid_username = False
                email =  "%s@socialauth" % (username)
            else:
                valid_username = True
            if email:
                qry = User.objects.filter(email=email)[:1]
                if len(qry) == 1:
                    user = qry[0]
            
            if not user:
                user = create_user_from_session(request,username,email)
                
                user.first_name = firstname
                user.last_name = lastname
                user.save()
            print 'user is registered with id ' + str(user.id)
    
            #create openid association
            assoc = UserAssociation()
            assoc.openid_key = openid_key
            assoc.user = user
            if email:
                assoc.email = email
            if nickname:
                assoc.nickname = nickname
            if valid_username:
                assoc.is_username_valid = True
            assoc.save()
            
            #Create AuthMeta
            # auth_meta = AuthMeta(user=user, provider=provider, provider_model='OpenidProfile', provider_id=assoc.pk)
            auth_meta = AuthMeta(user=user, provider=provider)
            auth_meta.save()
            return user
        
    def GooglesAX(self,openid_response):
        email = openid_response.ax.getSingle('http://axschema.org/contact/email')
        firstname = openid_response.ax.getSingle('http://axschema.org/namePerson/first')
        lastname = openid_response.ax.getSingle('http://axschema.org/namePerson/last')
        # country = openid_response.ax.getSingle('http://axschema.org/contact/country/home')
        # language = openid_response.ax.getSingle('http://axschema.org/pref/language')
        return locals()
  
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id)
            return user
        except User.DoesNotExist:
            return None

class LinkedInBackend:
    """LinkedInBackend for authentication"""
    def authenticate(self, request,linkedin_access_token, user=None):
        linkedin = LinkedIn(LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET)
        # get their profile
        
        profile = ProfileApi(linkedin).getMyProfile(access_token = linkedin_access_token)

        try:
            user_profile = LinkedInUserProfile.objects.get(linkedin_uid = profile.id)
            user = user_profile.user
            return user
        except LinkedInUserProfile.DoesNotExist:
            # Create a new user
            username = 'LI:%s' % profile.id

            if not user:
                user = create_user_from_session(request,username)
                user.first_name, user.last_name = profile.firstname, profile.lastname
                user.email = '%s@socialauth' % (username)
                user.save()
                
            userprofile = LinkedInUserProfile(user=user, linkedin_uid=profile.id)
            userprofile.save()
            
            auth_meta = AuthMeta(user=user, provider='LinkedIn').save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

class TwitterBackend:
    """TwitterBackend for authentication"""
    def authenticate(self,request ,twitter_access_token, user=None):
        '''authenticates the token by requesting user information from twitter'''
        # twitter = oauthtwitter.OAuthApi(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, twitter_access_token)
        twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        try:
            userinfo = twitter.get_user_info(twitter_access_token)
        except:
            # If we cannot get the user information, user cannot be authenticated
            raise

        screen_name = userinfo.screen_name
        twitter_id = userinfo.id
        
        try:
            user_profile = TwitterUserProfile.objects.get(screen_name=screen_name)
            
            # Update Twitter Profile
            user_profile.url = userinfo.url
            user_profile.location = userinfo.location
            user_profile.description = userinfo.description
            user_profile.profile_image_url = userinfo.profile_image_url
            user_profile.save()
            
            user = user_profile.user
            return user
        except TwitterUserProfile.DoesNotExist:
            # Create new user
            if not user:
                same_name_count = User.objects.filter(username__startswith=screen_name).count()
                if same_name_count:
                    username = '%s%s' % (screen_name, same_name_count + 1)
                else:
                    username = screen_name
                user = create_user_from_session(request,username)
                name_data = userinfo.name.split()
                try:
                    first_name, last_name = name_data[0], ' '.join(name_data[1:])
                except:
                    first_name, last_name =  screen_name, ''
                user.first_name, user.last_name = first_name, last_name
                #user.email = screen_name + "@socialauth"
                #user.email = '%s@example.twitter.com'%(userinfo.screen_name)
                user.save()
                
            user_profile = TwitterUserProfile(user=user, screen_name=screen_name)
            user_profile.access_token = twitter_access_token
            user_profile.url = userinfo.url
            user_profile.location = userinfo.location
            user_profile.description = userinfo.description
            user_profile.profile_image_url = userinfo.profile_image_url
            user_profile.save()
            
            auth_meta = AuthMeta(user=user, provider='Twitter').save()
                
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
        
class FacebookBackend:
    def authenticate(self, request, user=None):
        cookie = None
        try:
            cookie = facebook.get_user_from_cookie(request.COOKIES, FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY)
        except:
            traceback.print_exc()
        if cookie:
            uid = cookie['uid']
            access_token = cookie['access_token']
            fb_user = None
            fb_data = None
        else:
            print 'asking for access token'
            # if cookie does not exist
            # assume logging in normal way
            params = {}
            params["client_id"] = FACEBOOK_APP_ID
            params["client_secret"] = FACEBOOK_SECRET_KEY
            params["redirect_uri"] = request.build_absolute_uri(reverse("socialauth_facebook_login_done"))
            params["code"] = request.GET.get('code', '')

            url = "https://graph.facebook.com/oauth/access_token?"+urllib.urlencode(params)
            from cgi import parse_qs
            fp = urllib.urlopen(url)
            userdata = utils.read_urllib_fp_to_str(fp)
            res_parse_qs = parse_qs(userdata)
            # Could be a bot query
            if not res_parse_qs.has_key('access_token'):
                return None

            access_token = res_parse_qs['access_token'][-1]

            # create new FacebookUserProfile
            graph = facebook.GraphAPI(access_token)
            fb_data = graph.get_object("me")
            print fb_data
            uid = fb_data['id']
        try:
            fb_user = FacebookUserProfile.objects.get(facebook_uid=uid)
            u = fb_user.user
            return u
        except FacebookUserProfile.DoesNotExist:
        
            print 'user is not signed'
            if fb_data == None:
                graph = facebook.GraphAPI(access_token) 
                fb_data = graph.get_object("me")
            
            if not fb_data:
                return None

            email = fb_data['email']
            if email:
                username = email.split('@')[0]
                qry = User.objects.filter(email=email)[:1]
                if len(qry) == 1:
                    user = qry[0]
                    user.is_active = True
                    user.save()

            if not user:
                name_count = User.objects.filter(username__startswith = username).count()
                if name_count:
                    username = '%s%d' % (username, name_count + 1)
                else:
                    username = '%s' % (username)
                user = create_user_from_session(request,username)
                user.first_name = fb_data['first_name']
                user.last_name = fb_data['last_name']
                user.email = email
                user.save()

            fb_profile = FacebookUserProfile(facebook_uid=uid, user=user)
            fb_profile.save()

            ext = get_user_extension_from_request(user,request)
            ext.FB_ID = uid
            ext.FB_token = access_token
            ext.bio = fb_data.get('bio','')
            ext.website = fb_data.get('website','')
            print fb_data
            friends = []
            try:
                friends = graph.get_object('me/friends')
            except:
                pass
            if friends and friends.get('data',None):
                friends = friends.get('data')
            friend_list = ''.join(f['id'] + ',' for f in friends)
            ext.friends = friend_list

            interest = []
            try:
                interest = graph.get_object('me/interests')
            except Exception,e:
                pass
            if interest and interest.get('data') != None:
                interest = interest['data']
            print interest
            ext.interest = interest

            activities = []
            try:
                activities = graph.get_object('me/activities')
            except Exception,e:
                pass
            if activities and activities.get('data') != None:
                activities = activities['data']
            print activities
            ext.activities = activities

            events = []
            try:
                events = graph.get_object('me/events')
            except Exception,e:
                pass
            if events and events.get('data') != None:
                events = events['data']
            print events
            ext.events = events

            groups = []
            try:
                groups = graph.get_object('me/groups')
            except Exception,e:
                pass
            if groups and groups.get('data') != None:
                groups = groups['data']
            print groups
            ext.groups = groups

            if request.session.get('is_merchant',False):
                ext.is_merchant = True

            ext.save()

            auth_meta = AuthMeta(user=user, provider='Facebook').save()

            request.user_extension = ext
                
            return user

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None



def create_user_with_random_password(username, email=''):
    password = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in xrange(12)])
    user = User(username=username, email=email,password=password)
    return user

def create_user_from_session(request,username, email='', password=None):
    if not password:
        user = create_user_with_random_password(username,email)
    else:
        user = User.objects.create_user(username, email, password)
    old_func = user.save
    self = user
    def user_overriden_save(*args, **kwargs):
        ret = old_func(*args,**kwargs)
        session = request.session.session_key
        UserLog.user_logged_in(self,session)
        return ret

    user.save = user_overriden_save
    return user

def get_user_extension_from_request(user,request):
    qry = UserExtension.objects.filter(user=user)[:1]
    ext = None
    if len(qry) > 0:
        ext = qry[0]
    if not ext:
        ext = UserExtension.create_from_user(user)
        referrer = get_referrer_from_request(request)
        if referrer:
            ext.referred_by = referrer
            ext.referred_by_id = referrer.id
    if request.session.get('is_merchant'):
        ext.is_merchant = True
    return ext

def get_referrer_from_request(request):
    referrer_name = request.session.get('referrer')
    if referrer_name:
        try:
            return User.objects.get(username=referrer_name)
        except User.DoesNotExist:
            pass
    return None
