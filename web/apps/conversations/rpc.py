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

from conversations import models
from datetime import datetime, timedelta, date
from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist
from django.conf.global_settings import LANGUAGES
import stomp

# useful for stubbing during tests.
now = datetime.now

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])
LANGUAGE_DICT = dict(SORTED_LANGUAGES)

def _send_stomp(message, destination):
    conn = stomp.Connection(user='writer', passcode='writer')
    conn.start()
    conn.connect(wait=True)
    conn.send(json.dumps(message), destination=destination)
    conn.stop()

def find_match(request, near_id=None):
    waiting_user = models.WaitingUser.objects.get(user=request.user)
    if waiting_user.conversation:
        return _fulfilled_ping(waiting_user)
    match, lp = _find_matched_waiting_user(waiting_user)
    if match:
        conversation = models.Conversation(
            language_0=lp.native_language,
            language_1=lp.foreign_language,
            user_0=request.user,
            user_1=match.user,
            near_id_0=near_id,
            near_id_1=match.near_id)
        conversation.save()
        # TODO: start a channel
        match.conversation = conversation
        match.save()
        waiting_user.delete()
        # TODO: maybe save a CompletedWait here
        _send_stomp(
            { 'message_type': 'matched' },
            match.user.stomp_destination())
        return {
            'status': 'matched',
            'near_id': match.near_id }
    else:
        waiting_user.last_ping = now()
        waiting_user.save()
        return { 'status': 'unmatched' }

def ping_waiting(request, near_id=None):
    waiting_user, created = models.WaitingUser.objects.get_or_create(
        user=request.user,
        defaults={ 'near_id': near_id })
    if created:
        _save_language_pairs(waiting_user)
    if waiting_user.conversation:
        return _fulfilled_ping(waiting_user)
    else:
        waiting_user.update_last_ping(now())
        return { 'status': 'unmatched' }

def fetch_chart(request):
    try:
        waiting_user = models.WaitingUser.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return { 'text': '' }
    start_date = datetime.now() - timedelta(days=5)
    start_date = datetime(
        start_date.year, start_date.month,
        start_date.day, start_date.hour)
    language_pairs = []
    hourly_visits_dicts = []
    for lp in waiting_user.waitinguserlanguagepair_set.all():
        language_pairs.append(
            [LANGUAGE_DICT[lp.foreign_language], 
             LANGUAGE_DICT[lp.native_language]])
        hourly_visits = _hourly_visits_for(
            lp.foreign_language, lp.native_language, start_date)
        hourly_visits_dicts.append(
            dict([(str(hv.datetime), hv) for hv in hourly_visits]))
    csv_text = _csv_from_hourly_visits(
        language_pairs, hourly_visits_dicts, start_date)
    return { 'text': csv_text }

def ping_conversation(request):
    return {}

def _hourly_visits_for(native_language, foreign_language, start_date):
    return models.HourlyVisits.objects.filter(
        native_language=native_language,
        foreign_language=foreign_language,
        date__gte=start_date)

def _csv_from_hourly_visits(language_pairs, hourly_visits_dicts, start_date):
    end_date = datetime.now()
    rows = []
    header_row = ['Date']
    header_row.extend(
        ['"{0} speakers learning {1}"'.format(lp[0], lp[1]) 
         for lp in language_pairs])
    rows.append(','.join(header_row))
    cur_date = start_date
    while cur_date < end_date:
        row = []
        row.append(cur_date.strftime("%Y/%m/%d %H:00:00"))
        date_str = str(cur_date)
        for dict in hourly_visits_dicts:
            if date_str in dict:
                row.append(str(dict[date_str].count))
            else:
                row.append("0")
        rows.append(','.join(row))
        cur_date += timedelta(hours=1)
    return '\n'.join(rows)

def _save_language_pairs(waiting_user):
    waiting_user.waitinguserlanguagepair_set.all().delete()
    user = waiting_user.user
    for l in user.preferreduserlanguage_set.all():
        lp = models.WaitingUserLanguagePair(
            waiting_user=waiting_user,
            native_language=waiting_user.user.native_language,
            foreign_language=l.language)
        lp.save()

def _find_matched_waiting_user(waiting_user):
    cutoff = now() - timedelta(seconds=models.TIMEOUT)
    for lp in waiting_user.waitinguserlanguagepair_set.all():
        matched_lp_qs = models.WaitingUserLanguagePair.objects.filter(
            native_language=lp.foreign_language,
            foreign_language=lp.native_language,
            last_ping__gt=cutoff)
        if matched_lp_qs.count() > 0:
            matched_lp = matched_lp_qs[0]
            return matched_lp.waiting_user, matched_lp
    return None, None

def _fulfilled_ping(waiting_user):
    conversation = waiting_user.conversation
    waiting_user.delete()
    # TODO: possibly save a CompletedWait here.
    return {
        'status': 'matched',
        'near_id': conversation.near_id_0 }
