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

from django.http import HttpResponse, Http404, HttpResponseRedirect, QueryDict
from django.contrib.sites.models import Site
from llauth.models import CustomUser as User
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from datetime import datetime
import scheduling
from scheduling import models
from django.conf.global_settings import LANGUAGES
from django.core.urlresolvers import reverse

utcnow = datetime.utcnow

def ical_download(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    ical_text = scheduling.icalendar(
        user.native_languages(), user.foreign_languages())
    response = HttpResponse(ical_text, mimetype="text/calendar")
    response["Content-Disposition"] = "attachment; filename=langolab.ics"
    return response;

def googlecal(request, user_id):
    query_dict = QueryDict()
    query_dict['cid'] = "http://{0}{1}".format(
        Site.objects.get_current().domain,
        reverse('scheduling:ical', args=[user_id]))
    return redirect("http://www.google.com/calendar/render?{0}".format(
            query_dict.urlencode()))

def yahoocal(request, user_id):
    return HttpResponse('yahoocal')

def ical(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    ical_text = scheduling.icalendar(
        user.native_languages(), user.foreign_languages())
    return HttpResponse(ical_text, mimetype="text/calendar")

def email_test(request):
    dates = [[datetime(2011, 8, 11, 14), datetime(2011, 8, 11, 16), True],
             [datetime(2011, 8, 12, 21), datetime(2011, 8, 13, 2), False],
             [datetime(2011, 8, 14, 14), datetime(2011, 8, 14, 16), True],]
    context = { 'foreign_languages_text': 'German', 
                'native_languages_text': 'English',
                'times': dates, 
                'user_id': 42 }
    str = render_to_string(
        "scheduling/notification_email.html",
        context,
        context_instance=RequestContext(request))
    return render_to_response(
        "email_viewer.html",
        { 'email_html': str },
        context_instance=RequestContext(request))
