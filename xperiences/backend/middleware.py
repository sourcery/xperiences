from django.contrib.auth.models import AnonymousUser
from backend.models import UserExtension, UserLog
from django.utils.functional import SimpleLazyObject

__author__ = 'ishai'

class LazyUserExtension(object):
    def __get__(self, request, _=None):
        return request.user.get_profile()

class LazyMerchant(object):
    def __get__(self, request, _=None):
        if request.user_extension and request.user_extension.is_merchant:
            return request.user_extension
        else:
            return None


class UserExtensionMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.__class__.merchant = LazyMerchant()
        request.__class__.user_extension = LazyUserExtension()
        return None


class UserLogMiddleware(object):
    def process_request(self,request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        user = request.user
        url = request.get_full_path()
        if url.startswith('/admin') or url.startswith('/super_admin') or url.startswith('/media') or url.startswith('/static') or url.endswith('.ico'):
            return
        if user and not isinstance(user, AnonymousUser):
            log = UserLog.create_from_user(user,url)
            log.save()
        else:
            log = UserLog.create_from_session(request.session.session_key,url)
            log.save()



class ReferralMiddleware(object):
    def process_request(self,request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        if 'referrer' in request.GET:
            request.session['referrer'] = request.GET['referrer']

import settings
CONTEXT = { 'IP_GEOLOCATOR_API_KEY' : settings.IP_GEOLOCATOR_API_KEY, "settings": settings }
def context_processor(request):
    def auth(request):
        """
        Returns context variables required by apps that use Django's authentication
        system.

        If there is no 'user' attribute in the request, uses AnonymousUser (from
        django.contrib.auth).
        """
    # If we access request.user, request.session is accessed, which results in
    # 'Vary: Cookie' being sent in every request that uses this context
    # processor, which can easily be every request on a site if
    # TEMPLATE_CONTEXT_PROCESSORS has this context processor added.  This kills
    # the ability to cache.  So, we carefully ensure these attributes are lazy.
    # We don't use django.utils.functional.lazy() for User, because that
    # requires knowing the class of the object we want to proxy, which could
    # break with custom auth backends.  LazyObject is a less complete but more
    # flexible solution that is a good enough wrapper for 'User'.
    def get_user_extension():
        if hasattr(request, 'user_extension'):
            return request.user_extension
        else:
            return None
    def get_merchant():
        if hasattr(request, 'merchant'):
            return request.merchant
        else:
            return None

    CONTEXT['user_extension'] = SimpleLazyObject(get_user_extension)
    CONTEXT['merchant'] = SimpleLazyObject(get_merchant)
    return CONTEXT
