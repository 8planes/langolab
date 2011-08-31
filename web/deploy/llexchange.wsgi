import site
site.addsitedir('/home/llexchange/env/lib/python2.6/site-packages')

import sys
sys.path.append('/home/llexchange/llexchange/web')
sys.path.append('/home/llexchange/llexchange/web/apps')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'langolab_settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
