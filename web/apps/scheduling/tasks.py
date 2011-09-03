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

from celery.task import task
from datetime import date, datetime, timedelta
from scheduling import models
from llauth.models import CustomUser as User
from celery.signals import task_failure
from django.conf import settings
from celery.decorators import periodic_task
from user_notifier import notify_user
import string, random
import logging
import traceback as traceback_

# makes unit testing easier, since we can alter value returned by now.
now = datetime.now

# number of potential partners a user needs to warrant a notification
# hopefully we'll be able to increase this in the future.
NOTIFICATION_PARTNER_THRESHOLD = 5

# min number of hours in between notifications to a particular user.
MIN_NOTIFICATION_PERIOD = 48

_ALPHANUM = string.letters + string.digits

def process_failure_signal(exception, traceback, sender, task_id,  
                           signal, args, kwargs, einfo, **kw):  
    exc_info = (type(exception), exception, traceback)  
    traceback_.print_exception(exc_info[0], exc_info[1], exc_info[2])

task_failure.connect(process_failure_signal)

@task
def update_schedules(user_id, utc_start_date, num_hours):
    end_date = utc_start_date + timedelta(hours=num_hours)
    start_hour = models.LanguagePairUserCount.hour_for_date(utc_start_date)
    end_hour = models.LanguagePairUserCount.hour_for_date(end_date)
    user = User.objects.get(id=user_id)
    native_languages = [user.native_language];
    foreign_languages = [p.language for p in 
                         user.preferreduserlanguage_set.all()]
    # the flip is intentional here.
    for foreign_language in native_languages:
        for native_language in foreign_languages:
            _update_lp_schedule(start_hour, end_hour, 
                                native_language, foreign_language)

@periodic_task(run_every=timedelta(hours=3))
def notify_users():
    users = User.objects.filter(
        userschedulerange__end_time__gte=now()).distinct()
    for user in users:
        _maybe_notify_user(user)

def _maybe_notify_user(user):
    if models.UserNotificationOptOut.objects.filter(user=user).exists():
        return
    last_notification = user.usernotification_set.order_by('-date_sent')[:1]
    if len(last_notification) > 0:
        td = now() - last_notification[0].date_sent
        total_seconds = td.seconds + td.days * 24 * 3600
        if total_seconds / 3600 <= MIN_NOTIFICATION_PERIOD:
            return
    now_datetime = now()
    start_datetime = datetime(now_datetime.year, 
                              now_datetime.month,
                              now_datetime.day,
                              now_datetime.hour)
    user_counts = models.LanguagePairUserCount.user_counts(
        [user.native_language],
        [p.language for p in user.preferreduserlanguage_set.all()],
        start_datetime,
        start_datetime + timedelta(days=5))
    ranges_past_threshold = _ranges_past_threshold(start_datetime, user_counts)
    if len(ranges_past_threshold) > 0:
        if len(last_notification) == 0 or \
                _contains_new_ranges(ranges_past_threshold, last_notification[0]):
            _notify_user(user, ranges_past_threshold)

def _notify_user(user, ranges_past_threshold):
    user_notification = models.UserNotification(
        user=user,
        date_sent=now(),
        code=''.join([_ALPHANUM[random.randint(0, len(_ALPHANUM)-1)] 
                      for i in xrange(12)]))
    user_notification.save()
    for range in ranges_past_threshold:
        models.UserNotificationRange(notification=user_notification,
                                     start_time=range[0],
                                     end_time=range[1]).save()
    notify_user(user, ranges_past_threshold)

def _contains_new_ranges(ranges, last_notification):
    earliest_date = ranges[0][0]
    previous_ranges = \
        [[r.start_time, r.end_time] for r in 
         last_notification.usernotificationranges_set.filter(
            end_time__gte=earliest_date).all()]
    for range in ranges:
        if not _range_is_contained(range, previous_ranges):
            return True
    return False

def _range_is_contained(range, range_arr):
    for r in range_arr:
        if r[0] <= range[0] and r[1] >= range[1]:
            return True
    return False

def _ranges_past_threshold(start_datetime, user_counts):
    cur_range = None
    ranges = []
    cur_hour = 0
    date = None
    for user_count in user_counts:
        date = start_datetime + timedelta(hours=cur_hour)
        if user_count >= NOTIFICATION_PARTNER_THRESHOLD and cur_range is None:
            cur_range = [date, date]
        elif user_count >= NOTIFICATION_PARTNER_THRESHOLD:
            cur_range[1] = date
        elif user_count < NOTIFICATION_PARTNER_THRESHOLD and cur_range is not None:
            ranges.append(cur_range)
            cur_range = None
        cur_hour += 1
    if cur_range is not None:
        ranges.append(cur_range)
    return ranges

def _update_lp_schedule(start_hour, end_hour, 
                        native_language, foreign_language):
    start_date = models.LanguagePairUserCount.date_for_hour(start_hour)
    end_date = models.LanguagePairUserCount.date_for_hour(end_hour)
    models.LanguagePairUserCount.objects.filter(
        hour__gte=start_hour,
        hour__lte=end_hour,
        native_language=native_language,
        foreign_language=foreign_language).delete()
    users = User.objects.filter(
        native_language=foreign_language,
        preferreduserlanguage__language=native_language)
    user_counts = [0] * (end_hour - start_hour + 1)
    for user in users:
        for srange in user.userschedulerange_set.filter(
            start_time__lte=end_date, end_time__gte=start_date):
            for i in range(srange.start_hour, srange.end_hour + 1):
                user_counts[i - start_hour] += 1
    cur_hour = start_hour
    for user_count in user_counts:
        if user_count > 0:
            models.LanguagePairUserCount(
                hour=cur_hour,
                native_language=native_language,
                foreign_language=foreign_language,
                user_count=user_count).save()
        cur_hour += 1
