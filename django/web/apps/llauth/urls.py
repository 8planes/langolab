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
from django.core.urlresolvers import reverse

urlpatterns = patterns(
    'llauth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^twitter_login/', 'twitter_login', name='twitter_login'),
    url(r'^twitter_login_done/', 'twitter_login_done', name="twitter_login_done"),
    url(r'^maybe_logged_in/', 'maybe_logged_in', name='maybe_logged_in'),
    url(r'^create_user/$', 'create_user', name='create_user'),
    url(r'^login_post/$', 'login_post', name='login_post'),
    url(r'^simplified_signup/$', 'simplified_signup', name="simplified_signup"),
)

urlpatterns += patterns(
    '',
    url(r'^close_window/$', 
        'django.views.generic.simple.direct_to_template',
        {'template': 'llauth/close_window.html'}, name="close_window"),
    url(r'^password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        name='password_reset'),
)
