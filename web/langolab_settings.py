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

# production settings

from settings import *
from langolab_secret_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

JS_DEBUG = False

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'llexchange',
        'USER' : DB_USER,
        'PASSWORD' : DB_PASSWORD,
        'HOST' : '',
        'PORT' : ''
        }
    }

SITE_ID = 2
SITE_NAME = 'langolab'

STOMP_SERVER = 'www.langolab.com'

TWITTER_CONSUMER_KEY = 'c9dFh0Gua9qwWTDmEZIXQ'

FACEBOOK_APP_ID = '170317592993518'

MEDIA_URL = 'http://www.langolab.com/site_media/'
