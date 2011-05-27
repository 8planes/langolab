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
from django.conf.global_settings import LANGUAGES
from llauth.models import CustomUser as User
from datetime import timedelta, datetime, date
from django.db.models import Count

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])

TIMEOUT = 20 # 20 seconds

class Conversation(models.Model):
    TYPE_REGULAR = 1
    TYPE_20QUESTIONS = 2
    TYPES = (
        (TYPE_REGULAR, "Regular"),
        (TYPE_20QUESTIONS, "20 Questions"),
    )
    time_started = models.DateTimeField(auto_now_add=True)
    language_0 = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    language_1 = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    user_0 = models.ForeignKey(User, related_name="user_0")
    user_1 = models.ForeignKey(User, related_name="user_1")
    near_id_0 = models.CharField(max_length=255)
    near_id_1 = models.CharField(max_length=255)

class WaitingUser(models.Model):
    user = models.ForeignKey(User)
    time_started = models.DateTimeField(auto_now_add=True)
    last_ping = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, null=True)
    near_id = models.CharField(max_length=255)

    def update_last_ping(self, now):
        self.last_ping = now
        self.save()
        self.waitinguserlanguagepair_set.update(last_ping=now)

class WaitingUserLanguagePair(models.Model):
    waiting_user = models.ForeignKey(WaitingUser)
    native_language = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    foreign_language = models.CharField(max_length=16, choices=SORTED_LANGUAGES)
    last_ping = models.DateTimeField(auto_now_add=True)

class WaitingConversation(models.Model):
    waiting_user = models.ForeignKey(WaitingUser, null=False)    
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)

class ConversationsVisit(models.Model):
    user = models.ForeignKey(User)
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    arrive_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_date_seen = models.DateTimeField(auto_now_add=True)

class DailyVisits(models.Model):
    class Meta:
        unique_together = ("native_language", "foreign_language", "date")
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    date = models.DateField(db_index=True)
    count = models.IntegerField(default=0)

    @classmethod
    def save_daily_visits(cls, date):
        qs = ConversationsVisit.objects.filter(
            arrive_date__lt=date + timedelta(days=1),
            last_date_seen__gt=date).values(
            "native_language", "foreign_language").annotate(
            num_users=Count("user"))
        for item in qs:
            daily_visit, created = cls.objects.get_or_create(
                native_language=item['native_language'],
                foreign_language=item['foreign_language'],
                date=date,
                defaults=dict(count=item['num_users']))
            if not created:
                daily_visit.count = item['num_users']
                daily_visit.save()

class HourlyVisits(models.Model):
    class Meta:
        unique_together = ("native_language", "foreign_language", 
                           "date", "utc_hour_start")
    native_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    foreign_language = models.CharField(
        max_length=16, choices=SORTED_LANGUAGES, db_index=True)
    date = models.DateField()
    # utc_hour_start is 0-23.
    utc_hour_start = models.IntegerField()
    count = models.IntegerField(default=0)

    @property
    def datetime(self):
        return datetime(self.date.year, self.date.month, 
                        self.date.day, self.utc_hour_start)

    @classmethod
    def save_hourly_visits(cls, date):
        today = datetime(date.year, date.month, date.day)
        for hour in range(0, 24):
            qs = ConversationsVisit.objects.filter(
                arrive_date__lt=today + timedelta(hours=hour+1),
                last_date_seen__gt=today + timedelta(hours=hour)).values(
                "native_language", "foreign_language").annotate(
                num_users=Count("user"))
            for item in qs:
                hourly_visit, created = cls.objects.get_or_create(
                    native_language=item['native_language'],
                    foreign_language=item['foreign_language'],
                    date=date,
                    utc_hour_start=hour,
                    defaults=dict(count=item['num_users']))
                if not created:
                    hourly_visit.count = item['num_users']
                    hourly_visit.save()
                
def update_visit_stats(native_language, foreign_language):
    daily_visits, created = DailyVisits.objects.get_or_create(
        native_language=native_language,
        foreign_language=foreign_language,
        date=date.today(),
        defaults=dict(count=1))
    if not created:
        daily_visits.count += 1
        daily_visits.save()
    hour = datetime.now().hour
    hourly_visits, created = HourlyVisits.objects.get_or_create(
        native_language=native_language,
        foreign_language=foreign_language,
        date=date.today(),
        utc_hour_start=hour,
        defaults=dict(count=1))
    if not created:
        hourly_visits.count += 1
        hourly_visits.save()
