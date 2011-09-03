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

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
from llauth.models import PreferredUserLanguage, CustomUser as User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from llauth.decorators import profile_required
from llauth.forms import LanguageBlankFormset, LanguageFormset
from decorators import render_json
from conversations import models
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import stomp
from django.utils import simplejson as json
from conversations import rpc as rpc_module
from django.db.models import Sum
from django.conf.global_settings import LANGUAGES

WAIT_EXPIRATION = 30
CHECK_INTERVAL = 10

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])
LANGUAGE_DICT = dict(SORTED_LANGUAGES)

def index(request):
    qs = models.DailyVisits.objects.filter(
        date__gt=datetime.now() - timedelta(days=8)).values(
        "native_language", "foreign_language").annotate(
        total_count=Sum("count")).order_by("-total_count")[:5]
    daily_visits = list(qs)
    for daily_visit in daily_visits:
        daily_visit['native_language_name'] = \
            LANGUAGE_DICT[daily_visit['native_language']]
        daily_visit['foreign_language_name'] = \
            LANGUAGE_DICT[daily_visit['foreign_language']]
    return render_to_response(
        "index.html", 
        { 'daily_visits': daily_visits },
        context_instance=RequestContext(request));

@profile_required
def enter_conversations(request):
    if request.method == 'GET':
        languages = request.user.preferreduserlanguage_set.all()
        if len(languages) == 0:
            formset = LanguageBlankFormset()
        else:
            formset = LanguageFormset(instance=request.user)
        return render_to_response(
            "conversations/enter_conversations.html",
            { 'formset': formset },
            context_instance=RequestContext(request));
    else:
        formset = LanguageFormset(request.POST, instance=request.user)
        formset.save()
        return redirect('conversations:conversations')

@profile_required
def conversations(request):
    for foreign_language in request.user.preferreduserlanguage_set.all():
        # we update these in middleware but only when the session-length
        # cookie is not set. So it makes sense to update them when a user
        # arrives at the conversations page.
        models.update_visit_stats(
            request.user.native_language, 
            foreign_language.language)
    models.WaitingUser.objects.filter(user=request.user).delete()
    languages_json = json.dumps(
        [(l.language, l.language_name()) for l in  
         request.user.preferreduserlanguage_set.all()])
    flash_vars = json.dumps({
            'cirrus_url': settings.CIRRUS_URL,
            'stomp_login': 'reader',
            'stomp_password': 'reader',
            'stomp_server': settings.STOMP_SERVER,
            'stomp_port': settings.STOMP_PORT,
            'stomp_subscribe_destination': request.user.stomp_destination() });
    return render_to_response(
        "conversations/conversations.html",
        { "languages_json": languages_json,
          "flash_vars": flash_vars,
          'js_debug': settings.JS_DEBUG },
        context_instance=RequestContext(request));

@csrf_exempt
def rpc(request, method_name):
    args = { 'request': request }
    for k, v in request.POST.items():
        args[k.encode('ascii')] = json.loads(v)
    func = getattr(rpc_module, method_name)
    result = func(**args)
    return HttpResponse(json.dumps(result), "application/json")

