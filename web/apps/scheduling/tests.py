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

TIME_RANGE = 7 * 24

def _schedule_arg_for_times(start_end_pairs):
    return \
        [{ 'start': [2011, 8, p[0], p[1]],
           'end': [2011, 8, p[2], p[3]] } 
         for p in start_end_pairs]

def _index_for_hour(start_day, day, hour):
    return (day - start_day) * 24 + hour

def _indexes_for_times(start_end_pairs, start_day):
    hours = [0] * TIME_RANGE
    for pair in start_end_pairs:
        start_index = _index_for_hour(start_day, pair[0], pair[1])
        end_index = _index_for_hour(start_day, pair[2], pair[3]) + 1
        hours[start_index:end_index] = [1] * (end_index - start_index)
    return hours

class SchedulingTest(TestCase):

    fixtures = ['test.json']

    def setUp(self):
        # speaks en, learning es
        self.user_0 = CustomUser.objects.get(username='test')
        # speaks es, learning en
        self.user_1 = CustomUser.objects.get(username='jose')
        # speaks it, learning en and es
        self.user_2 = CustomUser.objects.get(username='ricardo')

    def test_save_my_schedule_basic(self):
        schedule_arg = _schedule_arg_for_times([[11, 17, 11, 17]])
        request = RequestMockup(self.user_0)
        # test passes if this doesn't throw exception
        rpc.save_schedule(request, schedule_arg, 2011, 8, 11, TIME_RANGE)

    def test_retrieve_schedule(self):
        schedule_arg = _schedule_arg_for_times([[11, 17, 11, 17]])
        request = RequestMockup(self.user_0)
        rpc.save_schedule(request, schedule_arg, 2011, 8, 11, TIME_RANGE)
        resulting_schedule = rpc.fetch_schedule(
            request, ['es'], ['en'], 2011, 8, 11, TIME_RANGE)
        for hour in range(0, 7 * 24):
            self.assertEqual(
                1 if hour == 17 else 0,
                resulting_schedule[hour])

    def test_double_up_schedule(self):
        # TODO: save schedule twice, on top of each other
        pass

    def test_disjoint_schedule(self):
        # TODO: save schedule twice, but disjoint
        pass

    def test_save_schedule_two_users(self):
        user_1_times = [[11, 17, 11, 20], [12, 17, 12, 20]]
        schedule_arg = _schedule_arg_for_times(user_1_times)
        request = RequestMockup(self.user_1)
        rpc.save_schedule(request, schedule_arg, 2011, 8, 11, TIME_RANGE)

        user_2_times = [[11, 19, 11, 20], [12, 13, 12, 19]]
        schedule_arg = _schedule_arg_for_times(user_2_times)
        request = RequestMockup(self.user_2)
        rpc.save_schedule(request, schedule_arg, 2011, 8, 11, TIME_RANGE)

        resulting_schedule = rpc.fetch_schedule(
            request, ['en'], ['es', 'it'], 2011, 8, 11, TIME_RANGE)
        user_1_indexes = _indexes_for_times(user_1_times, 11)
        user_2_indexes = _indexes_for_times(user_2_times, 11)
        indexes = [x[0] + x[1] for x in zip(user_1_indexes, user_2_indexes)]
        self.assertEqual(len(indexes), len(resulting_schedule))
        for i in range(0, len(indexes)):
            self.assertEqual(indexes[i], resulting_schedule[i])
