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

urlpatterns = patterns(
    'conversations.views',
    url(r'^$', 'index', name='index'),
    url(r'^enter_conversations/$', 'enter_conversations', name='enter_conversations'),
    url(r'^conversations/$', 'conversations', name='conversations'),
    url(r'^rpc/(\w+)$', 'rpc'),
)

urlpatterns += patterns(
    '',
    url(r'^swfdemo/', 'django.views.generic.simple.direct_to_template', 
        {'template':'conversations/swfdemo.html'}),
    url(r'^closewindow/$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'conversations/closewindow.html'}, name='closewindow'),
)
