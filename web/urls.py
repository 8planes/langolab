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

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^about/', 'django.views.generic.simple.direct_to_template', 
        {'template':'about.html'}, name="about"),
    url(r'^contact/', 'django.views.generic.simple.direct_to_template', 
        {'template':'contact.html'}, name="contact"),
    url(r'^calendar/', 'django.views.generic.simple.direct_to_template', 
        {'template':'calendar.html'}, name="calendar"),
    (r'^for_teachers/', include('marketing.urls', namespace="marketing")),
    (r'^llauth/', include('llauth.urls', namespace='llauth')),
    (r'^admin/', include(admin.site.urls)),
    (r'^socialauth/', include('socialauth.urls')),
    (r'', include('conversations.urls', namespace='conversations')),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^favicon\.ico$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 
          'path': 'images/favicon.ico', 
          'show_indexes': True}))
