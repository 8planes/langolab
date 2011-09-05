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

from datetime import datetime, timedelta
from django.conf.global_settings import LANGUAGES
from django.db.models import Q
from scheduling import models
from llauth.models import CustomUser as User
import string, random
import operator

# userful for testing
utcnow = datetime.utcnow

# We keep Language Calendars updated up to this many days in the future.
NUM_UPDATE_DAYS = 14
# number of potential partners a user needs to warrant a notification
# hopefully we'll be able to increase this in the future.
NOTIFICATION_PARTNER_THRESHOLD = 5
BASE_DATE = datetime(2011, 1, 1)
SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])

_ALPHANUM = string.letters + string.digits

def hour_for_date(utc_date):
    td = utc_date - BASE_DATE
    total_seconds = td.seconds + td.days * 24 * 3600
    return total_seconds / 3600

def date_for_hour(hour):
    return BASE_DATE + timedelta(hours=hour)

def user_counts(native_languages, foreign_languages, start_date, end_date):
    start_hour = hour_for_date(start_date)
    end_hour = hour_for_date(end_date)
    calendar = calendar_for_languages(native_languages, foreign_languages)
    return list(models.LanguageCalendarUserCount.objects.filter(
        hour__gte=start_hour,
        hour__lte=end_hour,
        calendar=calendar).order_by('hour'))

def calendar_for_languages(native_languages, foreign_languages):
    native_string = ','.join(sorted(native_languages))
    foreign_string = ','.join(sorted(foreign_languages))
    calendar = None
    try:
        calendar = models.LanguageCalendar.objects.get(
            native_languages=native_string,
            foreign_languages=foreign_string)
    except models.LanguageCalendar.DoesNotExist:
        calendar = models.LanguageCalendar(
            native_languages=native_string,
            foreign_languages=foreign_string)
        calendar.save()
        for native_language in native_languages:
            models.LanguageCalendarNativeLanguage(
                calendar=calendar, native_language=native_language).save()
        for foreign_language in foreign_languages:
            models.LanguageCalendarForeignLanguage(
                calendar=calendar, foreign_language=foreign_language).save()
        update_language_calendar(calendar)
    return calendar

def update_language_calendar(calendar):
    now_ = utcnow()
    start_datetime = datetime(now_.year, now_.month, now_.day, now_.hour)
    end_datetime = start_datetime + timedelta(days=NUM_UPDATE_DAYS)
    _fill_user_counts(calendar, start_datetime, end_datetime)
    _update_calendar_ranges(calendar, start_datetime, end_datetime)

def random_string():
    return ''.join([_ALPHANUM[random.randint(0, len(_ALPHANUM)-1)] 
                    for i in xrange(12)])

def _update_calendar_ranges(calendar, start_datetime, end_datetime):
    start_hour = hour_for_date(start_datetime)
    end_hour = hour_for_date(end_datetime) - 1
    user_counts = models.LanguageCalendarUserCount.objects.filter(
        calendar=calendar,
        hour__gte=start_hour,
        hour__lte=end_hour).order_by('hour')
    ranges_past_threshold = [{'range': [date_for_hour(r[0]), 
                                        date_for_hour(r[1])], 
                              'uid': None} for r 
                             in _ranges_past_threshold(user_counts)]
    _fill_in_uids(calendar, ranges_past_threshold)
    calendar.languagecalendarrange_set.filter(
        start_date__lte=end_datetime,
        end_date__gte=start_datetime).delete()
    for range in ranges_past_threshold:
        models.LanguageCalendarRange(
            calendar=calendar,
            uid=range['uid'],
            start_date=range['range'][0],
            end_date=range['range'][1]).save()

def _fill_in_uids(calendar, ranges_past_threshold):
    for range in ranges_past_threshold:
        cal_range_list = \
            calendar.languagecalendarrange_set.filter(
            start_date__lte=range['range'][1],
            end_date__gte=range['range'][0])[:1]
        if len(cal_range_list) > 0:
            range['uid'] = cal_range_list[0].uid
        else:
            range['uid'] = '{0}-{1}-{2}'.format(
                calendar.native_languages, 
                calendar.foreign_languages,
                random_string())

def _ranges_past_threshold(user_counts):
    cur_hour = 0
    cur_range = None
    ranges = []
    T = NOTIFICATION_PARTNER_THRESHOLD
    for user_count in user_counts:
        if cur_range is not None and user_count.hour > cur_range[1] + 1:
            ranges.append(cur_range)
            cur_range = None
        if user_count.user_count >= T and cur_range is None:
            cur_range = [user_count.hour, user_count.hour]
        elif user_count.user_count >= T:
            cur_range[1] = user_count.hour
        elif user_count < T and cur_range is not None:
            ranges.append(cur_range)
            cur_range = None
    if cur_range is not None:
        ranges.append(cur_range)
    return ranges                

def _fill_user_counts(calendar, start_datetime, end_datetime):
    """ Deletes existing LanguageCalendarUserCounts, makes new ones.  """
    foreign_language_queries = \
        [Q(preferreduserlanguage__language=n.native_language) for 
         n in calendar.languagecalendarnativelanguage_set.all()]
    native_language_queries = \
        [Q(native_language=f.foreign_language) for 
         f in calendar.languagecalendarforeignlanguage_set.all()]
    users = User.objects.filter(
        reduce(operator.or_, foreign_language_queries)).filter(
        reduce(operator.or_, native_language_queries)).filter(
        userschedulerange__end_time__gte=start_datetime).distinct()
    start_hour = hour_for_date(start_datetime)
    end_hour = hour_for_date(end_datetime)
    user_counts = [0] * (end_hour - start_hour + 1)
    for user in users:
        for srange in user.userschedulerange_set.filter(
            start_time__lte=end_datetime, end_time__gte=start_datetime):
            start = max(srange.start_hour, start_hour)
            end = min(srange.end_hour, end_hour) + 1
            for i in range(start, end):
                user_counts[i - start_hour] += 1
    models.LanguageCalendarUserCount.objects.filter(
        hour__gte=start_hour, hour__lte=end_hour,
        calendar=calendar).delete()
    cur_hour = start_hour
    for user_count in user_counts:
        if user_count > 0:
            models.LanguageCalendarUserCount(
                hour=cur_hour,
                calendar=calendar,
                user_count=user_count).save()
        cur_hour += 1
