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

from django.core.management.base import BaseCommand, CommandError
from conversations import models
from datetime import datetime, date, timedelta

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        count = 20
        for nl in ['en', 'it', 'es', 'ja']:
            for fl in ['en', 'it', 'es', 'ja']:
                self._insert_daily_visits(nl, fl, count)
                count -= 1

    def _insert_daily_visits(self, nl, fl, count):
        if nl == fl:
            return
        for day in range(1, 3):
            daily_visits = models.DailyVisits(
                native_language=nl,
                foreign_language=fl,
                date=date.today() - timedelta(days=day),
                count=count)
            daily_visits.save()
