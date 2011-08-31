"""
Langolab -- learn foreign languages by speaking with random native speakers over webcam.
Copyright (C) 2011 Adam Duston

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)

gettext_noop = lambda s: s

from django.conf import global_settings
lang_dict = dict(global_settings.LANGUAGES)
lang_dict['es-ar'] = gettext_noop(u'Spanish, Argentinian')
lang_dict['en-gb'] = gettext_noop(u'English, British')
lang_dict['pt-br'] = gettext_noop(u'Portuguese, Brazilian')
lang_dict['sr-latn'] = gettext_noop(u'Latin, Serbian')
lang_dict['zh-cn'] = gettext_noop(u'Chinese, Simplified')
lang_dict['zh-tw'] = gettext_noop(u'Chinese, Traditional')
lang_dict['eo'] = gettext_noop(u'Esperanto')
global_settings.LANGUAGES = tuple(i for i in lang_dict.items())

DEBUG = True
TEMPLATE_DEBUG = DEBUG

JS_DEBUG = True

ADMINS = (
    ('Adam Duston', 'aduston@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('ll.sqlite3'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# socialauth-related
OPENID_REDIRECT_NEXT = '/socialauth/openid/done/'

OPENID_SREG = {"required": "nickname, email", "optional":"postcode, country", "policy_url": ""}
OPENID_AX = [{"type_uri": "http://axschema.org/contact/email", "count": 1, "required": True, "alias": "email"},
             {"type_uri": "fullname", "count": 1 , "required": False, "alias": "fullname"}]

AUTHENTICATION_BACKENDS = (
    'llauth.backends.CustomUserBackend',
    'llauth.backends.FacebookBackend',
    'llauth.backends.TwitterBackend',
    'llauth.backends.OpenIdBackend',
    'django.contrib.auth.backends.ModelBackend',
)

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

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('media')+'/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fa%vubbh1f4o73)-!m)*1^551qa^8qj_4bwhllwfz3#hhgvxb6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'middleware.RegisterVisitMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    rel('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    'django.core.context_processors.request',
    "django.core.context_processors.media",
    "django.core.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    'context_processors.add_stuff',
)

INSTALLED_APPS = (
    'llauth',
    'socialauth',
    'marketing',
    'scheduling',
    'south',
    'openid_consumer',
    'djcelery',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'conversations',
    'django.contrib.admin',
)

LOGIN_URL = '/llauth/login/'
STOMP_SERVER = 'll.example.com'
STOMP_PORT = 61613
CIRRUS_URL = 'rtmfp://p2p.rtmfp.net/7bbaaf24e9c7e6ba4c405591-3c650c743f5a/'

CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

try:
    from settings_local import *
except:
    pass
