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

import scheduling
from scheduling import models, tasks
from datetime import date, datetime, timedelta

def save_schedule(request, utc_schedule, utc_year, utc_month, utc_day, num_hours):
    start_datetime = datetime(utc_year, utc_month, utc_day)
    end_datetime = start_datetime + timedelta(hours=num_hours)
    models.UserScheduleRange.objects.filter(
        user=request.user,
        start_time__lte=end_datetime,
        end_time__gte=start_datetime).delete()
    for range in utc_schedule:
        start = range['start']
        end = range['end']
        start_time = datetime(start[0], start[1], start[2], start[3])
        end_time = datetime(end[0], end[1], end[2], end[3])
        models.UserScheduleRange(
            user=request.user,
            start_time=start_time,
            end_time=end_time).save()
    tasks.update_schedules.delay(
        request.user.id, datetime(utc_year, utc_month, utc_day), 
        num_hours)

def fetch_schedule(request, native_languages, foreign_languages, utc_year, utc_month, utc_day, num_hours):
    start_date = datetime(utc_year, utc_month, utc_day)
    end_date = start_date + timedelta(hours=num_hours - 1)
    return [{'hour': c.hour, 'count': c.user_count} for c in
            scheduling.user_counts(
            native_languages, foreign_languages, start_date, end_date)]
