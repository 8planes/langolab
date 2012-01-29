import site
import sys

prev_sys_path = list(sys.path)

site.addsitedir('/home/llexchange/env/lib/python2.6/site-packages')

sys.path.append('/home/llexchange/llexchange/web')
sys.path.append('/home/llexchange/llexchange/web/apps')

new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'langolab_settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
