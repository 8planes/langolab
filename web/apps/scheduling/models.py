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
import scheduling

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])

class UserScheduleRange(models.Model):
    user = models.ForeignKey(User)
    date_saved = models.DateTimeField(auto_now_add=True)
    # UTC
    start_time = models.DateTimeField()
    # UTC
    end_time = models.DateTimeField()

    @property
    def start_hour(self):
        return scheduling.hour_for_date(self.start_time)

    @property
    def end_hour(self):
        return scheduling.hour_for_date(self.end_time)

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

class LanguageCalendar(models.Model):
    class Meta:
        unique_together = ('native_languages', 'foreign_languages')
    # native languages in alphabetical order, comma-delimited
    native_languages = models.CharField(max_length=255, db_index=True)
    # foreign languages in alphabetical order, comma-delimited
    foreign_languages = models.CharField(max_length=255, db_index=True)
    last_update = models.DateTimeField(auto_now_add=True)

class LanguageCalendarNativeLanguage(models.Model):
    class Meta:
        unique_together = ('calendar', 'native_language')
    calendar = models.ForeignKey(LanguageCalendar)
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)

class LanguageCalendarForeignLanguage(models.Model):
    class Meta:
        unique_together = ('calendar', 'foreign_language')
    calendar = models.ForeignKey(LanguageCalendar)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)

class LanguageCalendarRange(models.Model):
    class Meta:
        unique_together = ('calendar', 'start_date')
    calendar = models.ForeignKey(LanguageCalendar)
    uid = models.CharField(max_length=64)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)

class LanguageCalendarUserCount(models.Model):
    class Meta:
        unique_together = ('hour', 'calendar')

    # hour since midnight, January 1, 2011 UTC
    hour = models.IntegerField(db_index=True)
    calendar = models.ForeignKey(LanguageCalendar)
    user_count = models.IntegerField()
