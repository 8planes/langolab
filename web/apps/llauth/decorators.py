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

from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django.core.urlresolvers import reverse

def approved_required(f, redirect_field_name="redirect_to"):
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(
                "/?%s=%s" % 
                (redirect_field_name, 
                 urlquote(request.get_full_path())))
        elif not request.user.is_approved:
            return HttpResponseRedirect(
                reverse('conversations:waiting_list'))
        else:
            return f(request, *args, **kwargs)
    return decorator

def profile_required(f, redirect_field_name="redirect_to"):
    def decorator(request, *args, **kwargs):
        path = request.get_full_path()
        if not request.user.is_authenticated():
            return HttpResponseRedirect(
                '{0}?next={1}'.format(
                    reverse('llauth:login'),
                    path))
        elif not request.user.native_language:
            return HttpResponseRedirect(
                '{0}?next={1}'.format(
                reverse('llauth:profile'),
                path))
        else:
            return f(request, *args, **kwargs)
    return decorator
