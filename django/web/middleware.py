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

from conversations import models
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta

VISIT_COOKIE = 'll_visit_ids'

class RegisterVisitMiddleware(object):
    def process_response(self, request, response):
        if VISIT_COOKIE not in request.COOKIES:
            if hasattr(request, 'user') and \
                    self._can_make_visit_records(request.user):
                visit_ids_string = self._make_visit_records(request.user)
                response.set_cookie(VISIT_COOKIE, visit_ids_string)
        else:
            visit_ids = request.COOKIES[VISIT_COOKIE]
            # TODO: queue async in future.
            self._update_visit_records([int(id) for id in visit_ids.split(',')])
        return response

    def _update_visit_records(self, visit_ids):
        for id in visit_ids:
            try:
                visit_record = models.ConversationsVisit.objects.get(id=id)
                visit_record.last_date_seen = datetime.now()
                visit_record.save()
            except ObjectDoesNotExist:
                pass

    def _can_make_visit_records(self, user):
        if not user.is_authenticated():
            return False
        if not user.native_language:
            return False
        return user.preferreduserlanguage_set.all().exists()

    def _make_visit_records(self, user):
        visit_record_ids = []
        for foreign_language in user.preferreduserlanguage_set.all():
            visit_record = models.ConversationsVisit(
                user=user,
                native_language=user.native_language,
                foreign_language=foreign_language.language)
            visit_record.save()
            visit_record_ids.append(visit_record.id)
            models.update_visit_stats(
                user.native_language, foreign_language.language)
        return ','.join([str(id) for id in visit_record_ids])

