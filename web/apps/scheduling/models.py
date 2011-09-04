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

from django.db import models

from llauth.models import CustomUser as User
from django.conf.global_settings import LANGUAGES
from datetime import datetime, timedelta

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])

BASE_DATE = datetime(2011, 1, 1)

class UserScheduleRange(models.Model):
    user = models.ForeignKey(User)
    date_saved = models.DateTimeField(auto_now_add=True)
    # UTC
    start_time = models.DateTimeField()
    # UTC
    end_time = models.DateTimeField()

    @property
    def start_hour(self):
        return LanguagePairUserCount.hour_for_date(
            self.start_time)

    @property
    def end_hour(self):
        return LanguagePairUserCount.hour_for_date(
            self.end_time)

class LanguagePairUserCount(models.Model):
    class Meta:
        unique_together = ('hour', 'native_language', 'foreign_language')

    # hour since midnight, January 1, 2011 UTC
    hour = models.IntegerField(db_index=True)
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    user_count = models.IntegerField()

    @classmethod
    def hour_for_date(cls, utc_date):
        td = utc_date - BASE_DATE
        total_seconds = td.seconds + td.days * 24 * 3600
        return total_seconds / 3600

    @classmethod
    def date_for_hour(cls, hour):
        return BASE_DATE + timedelta(hours=hour)

    @classmethod
    def user_counts(cls, native_languages, foreign_languages, start_date, end_date):
        """ Returns an array of user_counts per hour. First index 
        corresponds to start_date, and last to end_date """
        start_hour = LanguagePairUserCount.hour_for_date(start_date)
        end_hour = LanguagePairUserCount.hour_for_date(end_date)
        hour_dicts = []
        for native_language in native_languages:
            for foreign_language in foreign_languages:
                schedules_qs = LanguagePairUserCount.objects.filter(
                    hour__gte=start_hour,
                    hour__lte=end_hour,
                    native_language=native_language,
                    foreign_language=foreign_language).all()
                hour_dicts.append(
                    dict([(str(s.hour), s.user_count) for s in schedules_qs]))
        user_counts = [0] * (end_hour - start_hour + 1)
        for hour in range(start_hour, end_hour + 1):
            str_hour = str(hour)
            for hour_dict in hour_dicts:
                if str_hour in hour_dict:
                    user_counts[hour - start_hour] += hour_dict[str_hour]
        return user_counts

class UserNotificationOptOut(models.Model):
    user = models.ForeignKey(User)
    opt_out_date = models.DateTimeField(auto_now_add=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User)
    date_sent = models.DateTimeField(db_index=True)
    code = models.CharField(max_length=32)
    date_clicked = models.DateTimeField(null=True)

class UserNotificationRange(models.Model):
    notification = models.ForeignKey(UserNotification)
    # UTC
    start_time = models.DateTimeField()
    # UTC
    end_time = models.DateTimeField()
