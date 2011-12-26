import urlparse
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs

def user_extension_required(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user_extension:
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                           settings.LOGIN_REDIRECT_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url or settings.LOGIN_REDIRECT_URL, redirect_field_name)
        return _wrapped_view
    return decorator

def merchant_required(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.merchant:
                if request.merchant.is_approved:
                    return view_func(request, *args, **kwargs)
                else:
                    path = request.build_absolute_uri()
                    # If the login url is the same scheme and net location then just
                    # use the path as the "next" url.
                    login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                                   settings.MERCHANT_LOGIN_URL)[:2]
                    current_scheme, current_netloc = urlparse.urlparse(path)[:2]
                    if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                        path = request.get_full_path()
                    from django.contrib.auth.views import redirect_to_login
                    return redirect_to_login(path,'/merchants/register/',redirect_field_name)
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                           settings.MERCHANT_LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url or settings.MERCHANT_LOGIN_URL, redirect_field_name)
        return _wrapped_view
    return decorator