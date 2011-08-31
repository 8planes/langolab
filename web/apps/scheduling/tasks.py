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
import logging
import traceback as traceback_

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
    foreign_languages = [p.language for p in user.preferreduserlanguage_set.all()]
    # the flip is intentional here.
    for foreign_language in native_languages:
        for native_language in foreign_languages:
            _update_lp_schedule(start_hour, end_hour, native_language, foreign_language)
    
def _update_lp_schedule(start_hour, end_hour, native_language, foreign_language):
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
