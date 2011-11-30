from backend.models import UserExtension

__author__ = 'ishai'

class LazyUserExtension(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user_ext'):
            try:
                request._cached_user_ext = UserExtension.objects.get(user=request.user)
            except UserExtension.DoesNotExist:
                request._cached_user_ext = None
        return request._cached_user_ext

class LazyMerchant(object):
    def __get__(self, request, obj_type=None):
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


  