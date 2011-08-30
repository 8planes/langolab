from django.db import models

from llauth.models import CustomUser as User
from django.conf.global_settings import LANGUAGES

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])

class UserScheduleRange(models.Model):
    user = models.ForeignKey(User)
    date_saved = models.DateTimeField(auto_now_add=True)
    # UTC
    start_time = models.DateTimeField()
    # UTC
    end_time = models.DateTimeField()

class LanguagePairSchedule(models.Model):
    # hour since midnight, January 1, 2011 UTC
    hour = models.IntegerField()
    native_language = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    foreign_language = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    user_count = models.IntegerField()

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
