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

from django import forms
from llauth.models import CustomUser as User, PreferredUserLanguage
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

class ProfileFormWithEmail(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'native_language',)

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('native_language',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirm password'

LanguageBlankFormset = inlineformset_factory(User, PreferredUserLanguage, extra=1)
LanguageFormset = inlineformset_factory(User, PreferredUserLanguage, extra=0)
