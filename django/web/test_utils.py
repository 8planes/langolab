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

from django.test.client import Client
from django.core.urlresolvers import reverse
from llauth.models import CustomUser as User

def create_user(name, native_languages, foreign_languages):
    client = Client()
    response = client.post(
        reverse('llauth:create_user'), 
        { 'email': '{0}@example.com'.format(name),
          'next': '/enter_conversations/',
          'password1': 'cdbzb',
          'password2': 'cdbzb',
          'username': name })
    client.post(
        reverse('llauth:profile'),
        { 'native_language': native_languages[0],
          'next': '/enter_conversations/' })
    foreign_language_dict = {
        'preferreduserlanguage_set-TOTAL_FORMS': str(len(foreign_languages)),
        'preferreduserlanguage_set-INITIAL_FORMS': '0',
        'preferreduserlanguage_set-MAX_NUM_FORMS': '' }
    i = 0
    for fl in foreign_languages:
        foreign_language_dict.update(
            { 'preferreduserlanguage_set-{0}-id'.format(i): '',
              'preferreduserlanguage_set-{0}-language'.format(i): fl })
        i += 1
    client.post(
        reverse('conversations:enter_conversations'),
        foreign_language_dict)
    return User.objects.get(username=name)
