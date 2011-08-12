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
from scheduling import rpc
from datetime import datetime
from django.utils import simplejson as json
import time


# FIXME: duplicated from conversations/tests
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


class SchedulingTest(TestCase):

    fixtures = ['test.json']

    def setUp(self):
        # speaks en, learning es
        self.user_0 = CustomUser.objects.get(username='test')
        # speaks es, learning en
        self.user_1 = CustomUser.objects.get(username='jose')

    def test_save_my_schedule_basic(self):
        start_time = time.mktime(datetime(2011, 8, 11, 17).timetuple())
        end_time = time.mktime(datetime(2011, 8, 11, 17).timetuple())
        schedule_obj = [
            { 'start': start_time,
              'end': end_time }]
        jsonText = json.dumps(schedule_obj)
        request = RequestMockup(
            self.user_0, 
            post={'schedule': jsonText})
        # test passes if this doesn't throw exception
        rpc.save_schedule(request, schedule_obj)

