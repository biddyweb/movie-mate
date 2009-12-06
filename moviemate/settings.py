# Django settings for moviemate project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
APP_PATH = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

#DiscoSoup's edlab database connection
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'cs445_2_f09'
DATABASE_USER = 'cs445_2_f09'
DATABASE_PASSWORD = 'gwalter'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '3307'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/cs320dev/Dev/db/moviemate/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://imac.discosoup.net/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/dev-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pw+b#-$z#ug+vqawsrn-8*-38uy2j1ehr4^=1=bh+$x7$2%c_='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'moviemate.urls'
LOGIN_REDIRECT_URL = '/templates/home/'
LOGIN_URL = '/templates/login/'
LOGOUT_URL = '/templates/logout/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    APP_PATH + '/templates/',
)

AUTHENTICATION_BACKENDS = (
#    "moviemate.authentication.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

INSTALLED_APPS = (
    'moviemate',
    'moviemate.urlsMap',
    'moviemate.models',
    'moviemate.authentication',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
)
