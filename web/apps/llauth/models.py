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

from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.conf.global_settings import LANGUAGES
from django.db.models.signals import post_save
import StringIO

SORTED_LANGUAGES = list(LANGUAGES)
SORTED_LANGUAGES.sort(key=lambda item: item[1])
LANGUAGE_DICT = dict(SORTED_LANGUAGES)

class CustomUser(BaseUser):
    objects = UserManager()

    nickname = models.CharField(max_length=32, blank=True)
    is_approved = models.BooleanField(default=False)
    native_language = models.CharField(max_length=16, choices=SORTED_LANGUAGES, verbose_name='language', blank=True)
    profile_photo_url = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User'

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        if self.first_name:
            if self.last_name:
                return '{0} {1}'.format(
                    self.first_name, self.last_name[0])
            else:
                return self.first_name
        return self.username

    def stomp_destination(self):
        return '/user/{0}'.format(self.id)

def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()
        
post_save.connect(create_custom_user, BaseUser)

class PreferredUserLanguage(models.Model):
    user = models.ForeignKey(CustomUser)
    language = models.CharField(max_length=16, choices=SORTED_LANGUAGES, verbose_name='languages')

    def language_name(self):
        return LANGUAGE_DICT[self.language]
    
    class Meta:
        unique_together = ['user', 'language']
