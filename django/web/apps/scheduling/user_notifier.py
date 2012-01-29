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

from django.conf import settings
from boto.ses import SESConnection
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, redirect

def notify_user(user_notification):
    email = user_notification.user.email
    email_body = _body(user_notification)
    email_subject = _subject(user_notification)
    if settings.DEBUG:
        print("Sending email: {0} with subject: {1} to: {2}".format(
                email_string, email_subject, email))
    else:
        connection = SESConnection(
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY)
        connection.send_email(
            source="scheduling@langolab.com",
            subject=email_subject,
            body=email_body,
            to_addresses=[email],
            format='html',
            cc_addresses=['scheduling@langolab.com'])

def _subject(user_notification):
    pass

def _body(user_notification):
    pass
