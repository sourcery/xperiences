from django.contrib.auth.models import AnonymousUser
from backend.models import UserExtension, UserLog

__author__ = 'ishai'

class LazyUserExtension(object):
    def __get__(self, request, _=None):
        if not hasattr(request, '_cached_user_ext'):
            if request.user and not isinstance(request.user,AnonymousUser):
                try:
                    request._cached_user_ext = UserExtension.objects.get(user=request.user)
                except UserExtension.DoesNotExist:
                    request._cached_user_ext = None
            else:
                request._cached_user_ext = None
        return request._cached_user_ext

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
        if url.startswith('/admin') or url.startswith('/media') or url.startswith('/static') or url.endswith('.ico'):
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

