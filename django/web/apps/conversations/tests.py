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

from django.test import TestCase
from llauth.models import CustomUser
from django.core.urlresolvers import reverse
from conversations import rpc, models
from django.utils import simplejson as json
from datetime import datetime, timedelta, date

class RequestMockup(object):
    def __init__(self, user, get={}, post={}):
        self.user = user
        self.GET = get
        self.POST = post
        self.session = {}

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

class HookUpTest(TestCase):

    fixtures = ['test.json']

    def setUp(self):
        self.user_0 = CustomUser.objects.get(username='test')
        self.user_1 = CustomUser.objects.get(username='jose')
        self.request_0 = RequestMockup(
            self.user_0, 
            get={ 'langs': 'es,it' })
        self.request_1 = RequestMockup(
            self.user_1,
            get={ 'langs': 'en' })
        self.messages = []
        def send_stomp(message, destination):
            self.messages.append((message, destination))
        rpc._send_stomp = send_stomp

    def test_regular_hook_up(self):
        self._assert_ping(0, False, 'a')
        self._assert_find(0, False, 'a')
        self._assert_ping(0, False)
        self._assert_ping(1, False, 'b')
        self._assert_find(1, True, 'b')
        self._assert_ping(0, True)
        self._assert_matched_message(1, 3)

    def test_p0f0p1f1(self):
        self._assert_ping(0, False, 'a')
        self._assert_find(0, False, 'a')
        self._assert_ping(1, False, 'b')
        self._assert_find(1, True, 'b')
        self._assert_ping(0, True)
        self._assert_matched_message(1, 3)

    def test_p0p1f0f1(self):
        self._assert_ping(0, False, 'a')
        self._assert_ping(1, False, 'b')
        self._assert_find(0, True, 'a')
        self._assert_find(1, True, 'b')
        self._assert_matched_message(1, 4)

    def test_p0p1f1f0(self):
        self._assert_ping(0, False, 'a')
        self._assert_ping(1, False, 'b')
        self._assert_find(1, True, 'b')
        self._assert_find(0, True, 'a')
        self._assert_matched_message(1, 3)

    def _assert_ping(self, request_no, matched, near_id=None):
        self._assert_request(lambda r: rpc.ping_waiting(r, '1,2,3', near_id),
                             request_no,
                             matched)

    def _assert_find(self, request_no, matched, near_id=None):
        self._assert_request(lambda r: rpc.find_match(r, near_id),
                             request_no,
                             matched)

    def _assert_request(self, f, request_no, matched):
        request = self.request_0 if request_no == 0 else self.request_1
        content = f(request)
        self.assertEqual(
            'matched' if matched else 'unmatched',
            content['status'])

    def _assert_matched_message(self, num_messages, user_id):
        self.assertEqual(num_messages, len(self.messages))
        self.assertEqual('matched', self.messages[0][0]['message_type'])
        self.assertEqual('/user/{0}'.format(user_id), self.messages[0][1])

class VisitSummariesTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.user_0 = CustomUser.objects.get(username='test')

    def test_daily_visits(self):
        for nl in ['en', 'de']:
            for fl in ['en', 'it', 'es']:
                self._save_daily_visits(nl, fl)
        models.DailyVisits.save_daily_visits(date.today())
        self.assertEquals(5, models.DailyVisits.objects.count())
        for daily_visit in models.DailyVisits.objects.all():
            self.assertEquals(3, daily_visit.count)

    def test_hourly_visits(self):
        for nl in ['en', 'de']:
            for fl in ['en', 'it', 'es']:
                self._save_daily_visits(nl, fl)
        models.HourlyVisits.save_hourly_visits(date.today())
        self.assertEquals(15, models.HourlyVisits.objects.count())
        for hourly_visit in models.HourlyVisits.objects.all():
            self.assertEquals(1, hourly_visit.count)

    def test_csv(self):
        self._save_daily_visits('en', 'it', date.today() - timedelta(days=4))
        models.HourlyVisits.save_hourly_visits(date.today() - timedelta(days=4))
        self.assertEquals(3, models.HourlyVisits.objects.count())
        self.user_0 = CustomUser.objects.get(username='ricardo')
        request = RequestMockup(self.user_0)
        rpc.ping_waiting(request, "1,2,3", "a")
        data = rpc.fetch_chart(request)
        

    def _save_daily_visits(self, native_language, foreign_language, start_date=None):
        if native_language == foreign_language:
            return
        if start_date is None:
            today = date.today()
        else:
            today = start_date
        today = datetime(today.year, today.month, today.day)
        for hour in [2, 4, 8]:
            visit = models.ConversationsVisit(
                user=self.user_0,
                native_language=native_language,
                foreign_language=foreign_language)
            visit.save()
            visit.arrive_date = today + timedelta(hours=hour)
            visit.last_date_seen = today + timedelta(hours=hour+1)
            visit.save()

    
