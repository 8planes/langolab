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

class UserNotification(models.Model):
    user = models.ForeignKey(User)
    date_sent = models.DateTimeField()
    code = models.CharField(max_length=32)
    date_clicked = models.DateTimeField(null=True)

class UserNotificationRanges(models.Model):
    notification = models.ForeignKey(UserNotification)
    # UTC
    start_time = models.DateTimeField()
    # UTC
    end_time = models.DateTimeField()
    num_users = models.IntegerField()
