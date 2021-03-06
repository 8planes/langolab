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
from django.db.models import Q
import operator
import logging
import traceback as traceback_
import scheduling
from scheduling import NOTIFICATION_PARTNER_THRESHOLD

# makes unit testing easier, since we can alter value returned by utcnow.
utcnow = datetime.utcnow

# min number of hours in between notifications to a particular user.
MIN_NOTIFICATION_PERIOD = 48


def process_failure_signal(exception, traceback, sender, task_id,  
                           signal, args, kwargs, einfo, **kw):  
    exc_info = (type(exception), exception, traceback)  
    traceback_.print_exception(exc_info[0], exc_info[1], exc_info[2])

task_failure.connect(process_failure_signal)

@task
def update_schedules(user_id, utc_start_date, num_hours):
    end_date = utc_start_date + timedelta(hours=num_hours)
    start_hour = scheduling.hour_for_date(utc_start_date)
    end_hour = scheduling.hour_for_date(end_date)
    user = User.objects.get(id=user_id)
    foreign_language_queries = \
        [Q(languagecalendarforeignlanguage__foreign_language=nl)
         for nl in user.native_languages()]
    native_language_queries = \
        [Q(languagecalendarnativelanguage__native_language=fl)
         for fl in user.foreign_languages()]
    calendars = models.LanguageCalendar.objects.filter(
        reduce(operator.or_, foreign_language_queries)).filter(
        reduce(operator.or_, native_language_queries)).distinct()
    for calendar in calendars:
        scheduling.update_language_calendar(calendar)

@periodic_task(run_every=timedelta(hours=3))
def notify_users():
    users = User.objects.filter(
        userschedulerange__end_time__gte=utcnow()).distinct()
    for user in users:
        _maybe_notify_user(user)

def _maybe_notify_user(user):
    if models.UserNotificationOptOut.objects.filter(user=user).exists():
        return
    last_notification = user.usernotification_set.order_by('-date_sent')[:1]
    if len(last_notification) > 0:
        td = utcnow() - last_notification[0].date_sent
        total_seconds = td.seconds + td.days * 24 * 3600
        if total_seconds / 3600 <= MIN_NOTIFICATION_PERIOD:
            return
    now_datetime = utcnow()
    start_datetime = datetime(now_datetime.year, 
                              now_datetime.month,
                              now_datetime.day,
                              now_datetime.hour)
    calendar = scheduling.calendar_for_languages(
        user.native_languages(), user.foreign_languages())
    ranges_past_threshold = calendar.languagecalendarrange_set.filter(
        end_date__gte=start_datetime).order_by('start_date')
    if len(ranges_past_threshold) > 0:
        if len(last_notification) == 0 or \
                _contains_new_ranges(ranges_past_threshold, last_notification[0]):
            _notify_user(user, ranges_past_threshold)

def _notify_user(user, ranges_past_threshold):
    user_notification = models.UserNotification(
        user=user,
        date_sent=utcnow(),
        code=scheduling.random_string())
    user_notification.save()
    for range in ranges_past_threshold:
        models.UserNotificationRange(notification=user_notification,
                                     start_time=range.start_date,
                                     end_time=range.end_date).save()
    notify_user(user_notification)

def _contains_new_ranges(ranges, last_notification):
    earliest_date = ranges[0].start_date
    previous_ranges = \
        [[r.start_time, r.end_time] for r in 
         last_notification.usernotificationrange_set.filter(
            end_time__gte=earliest_date).all()]
    for range in ranges:
        if not _range_is_contained(range, previous_ranges):
            return True
    return False

def _range_is_contained(language_calendar_range, range_arr):
    for r in range_arr:
        if r[0] <= language_calendar_range.start_date and \
                r[1] >= language_calendar_range.end_date:
            return True
    return False
