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

from django.forms import ModelForm
from marketing.models import LLExchangeInterest
from django.core.mail import send_mail

class LLExchangeInterestForm(ModelForm):
    class Meta:
        model = LLExchangeInterest

    def send(self):
        text = "Interest from \n\n{0}\n\n{1}\n\n{2}\n\n{3}".format(
            self.cleaned_data['name'],
            self.cleaned_data['school'],
            self.cleaned_data['position'],
            self.cleaned_data['email'])
        send_mail('Langolab interest received',
                  text,
                  'noreply@langolab.com',
                  ['aduston@gmail.com'])

    def get_errors(self):
        from django.utils.encoding import force_unicode
        output = {}
        for key, value in self.errors.items():
            output[key] = '/n'.join([force_unicode(i) for i in value])
        return output
