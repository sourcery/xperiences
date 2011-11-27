# Django settings for Experience project.
import os
CODE_ROOT = os.path.dirname(__file__)

PRODUCTION = 'MONGOLAB_URI' in os.environ

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

import urlparse
if PRODUCTION:
    _DB_PARAMS = urlparse.urlparse(os.environ['MONGOLAB_URI'].replace('mongodb', 'http'))
    DATABASES = {
        'default': {
            'ENGINE': 'django_mongodb_engine',
            'NAME': _DB_PARAMS[2][1:],
            'USER': _DB_PARAMS.username,
            'PASSWORD': _DB_PARAMS.password,
            'HOST': _DB_PARAMS.hostname,
            'PORT': _DB_PARAMS.port,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django_mongodb_engine',
            'NAME': 'xperiences',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '27017',
        }
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


SITE_ID = '4eba73fe96cf4c019c00001d' if PRODUCTION else '4ece2ad476a6f60b0000001d'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


HTTP_BASE_URL = 'dev.empeeric.com/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = '-bp&vh3j4bv@kglrs2(u5qik-4p^ibp@ipuy&#z$_h0nxy%!!z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'backend.middleware.UserExtensionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'middleware.MongoMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "socialauth.context_processors.facebook_api_key",
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",

)

ROOT_URLCONF = 'xperiences.urls'

TEMPLATE_DIRS = (
    os.path.join(CODE_ROOT, 'templates'),
    os.path.join(CODE_ROOT, 'experiences/templates'),
    os.path.join(CODE_ROOT, 'merchants/templates'),
    os.path.join(CODE_ROOT, 'socialauth/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'backend',
    'experiences',
    'merchants',
    'djangotoolbox',
    'socialauth',
    'openid_consumer',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'socialauth.auth_backends.OpenIdBackend',
    'socialauth.auth_backends.TwitterBackend',
    'socialauth.auth_backends.FacebookBackend',
    'socialauth.auth_backends.LinkedInBackend',
    'backend.auth_backends.SimpleAuthBackend',
)

STATIC_DOC_ROOT = os.path.join(CODE_ROOT, 'media')
UPLOADED_IMAGES = os.path.join(CODE_ROOT, 'uploaded_media', 'images')
MEDIA_URL = "/media/"


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


FACEBOOK_APP_ID = '299479036742472'
FACEBOOK_API_KEY = '299479036742472'
FACEBOOK_SECRET_KEY = '498f25f7cb732faf01e9a197fedaf3a6'
FACEBOOK_PERMISSIONS = 'user_about_me,email,user_website,publish_stream,user_activities,user_birthday,user_education_history,user_events,user_groups,user_hometown,user_interests'

if DEBUG:
    FACEBOOK_APP_ID = '185047278245686'
    FACEBOOK_API_KEY = '185047278245686'
    FACEBOOK_SECRET_KEY = '378d3a53d53bb4947517892f4a812907'

EMAIL_HOST_USER = 'peeri.empeeric@gmail.com'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_PASSWORD = 'peeriempeeri'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

SERVER_EMAIL = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_URL = '/accounts/login/'


#Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJYBGEQMSD3MMPTYA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'my_prod_xpr_uploads' if PRODUCTION else 'my_dev_xpr_uploads'

SITE_CONFIGURATION_FILE = 'conf'
