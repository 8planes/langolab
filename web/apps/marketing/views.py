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

from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from marketing.forms import LLExchangeInterestForm
from django.utils import simplejson

def index(request):
    return render_to_response(
        'marketing/index.html',
        { 'form': LLExchangeInterestForm(),
          'fb_appid': settings.FACEBOOK_APP_ID},
        context_instance=RequestContext(request))

def interest(request):
    output = dict(success=False)
    form = LLExchangeInterestForm(request.POST)
    if form.is_valid():
        if not settings.DEBUG:
            form.send()
        form.save()
        output['success'] = True
    else:
        output['errors'] = form.get_errors()
    return HttpResponse(simplejson.dumps(output), 'text/javascript')
