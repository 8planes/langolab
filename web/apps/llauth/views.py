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

from __future__ import absolute_import
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from llauth.models import CustomUser as User
from llauth.forms import ProfileForm, ProfileFormWithEmail
from django.http import HttpResponseRedirect
from decorators import render_json
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from socialauth.views import get_url_host
from django.core.urlresolvers import reverse
import urllib
from django.conf import settings
from socialauth.lib import oauthtwitter2 as oauthtwitter
from django.http import HttpResponse
from oauth import oauth
from urllib2 import URLError
from django.contrib import messages
from django.contrib.sites.models import Site
from llauth.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

NoSuffixAuthenticationForm = \
    lambda **kwargs: AuthenticationForm(prefix="login", label_suffix="", **kwargs)

def login(request, next='/'):
    next = request.GET.get('next', next)
    return _render_login(
        request,
        CustomUserCreationForm(),
        NoSuffixAuthenticationForm(),
        next)

def login_post(request):
    redirect_to = request.POST['next']
    form = NoSuffixAuthenticationForm(data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)
    else:
        return _render_login(
            request,
            CustomUserCreationForm(),
            form,
            redirect_to)

def create_user(request):
    redirect_to = request.POST['next']
    form = CustomUserCreationForm(data=request.POST)
    if form.is_valid():
        new_user = form.save()
        user = authenticate(username=new_user.username,
                            password=form.cleaned_data['password1'])
        auth_login(request, user)
        return HttpResponseRedirect(redirect_to)
    else:
        return _render_login(
            request,
            form,
            NoSuffixAuthenticationForm(),
            redirect_to)

def simplified_signup(request):
    return render_to_response(
        'llauth/simplified_signup.html',
        { 'form': CustomUserCreationForm() },
        context_instance=RequestContext(request))

def _render_login(request, creation_form, login_form, redirect_to):
    return render_to_response(
        'llauth/login.html',
        { 'next': redirect_to,
          'login_form': login_form,
          'creation_form': creation_form },
        context_instance=RequestContext(request))

@login_required
def profile(request):
    if request.method == "POST":
        if request.user.email:
            form = ProfileForm(request.POST, instance=request.user)
        else:
            form = ProfileFormWithEmail(request.POST, instance=request.user)
        next = request.POST['next']
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.POST.get('next', '/'))
    else:
        if request.user.email:
            form = ProfileForm()
        else:
            form = ProfileFormWithEmail()
        next = request.GET.get('next', '/')
    return render_to_response(
        'llauth/profile.html',
        {'form': form, 'next': next},
        context_instance = RequestContext(request))

def twitter_login(request, next=None):
    callback_url = None
    next = request.GET.get('next', next)
    if next is None:
        next = 'http://{0}'.format(Site.objects.get_current().domain)

    callback_url = 'http://%s%s?next=%s' % \
        (Site.objects.get_current().domain,
         reverse("llauth:twitter_login_done"),
         urllib.quote(next))

    twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    request_token = twitter.fetch_request_token(callback_url)
    request.session['request_token'] = request_token.to_string()
    signin_url = twitter.authorize_token_url(request_token)
    return HttpResponseRedirect(signin_url)

def twitter_login_done(request):
    request_token = request.session.get('request_token', None)
    oauth_verifier = request.GET.get("oauth_verifier", None)

    # If there is no request_token for session,                                                                                                      
    # Means we didn't redirect user to twitter                                                                                                       
    if not request_token:
        # Redirect the user to the login page,                                                                                                       
        # So the user can click on the sign-in with twitter button                                                                                   
        return HttpResponse("We didn't redirect you to twitter...")

    token = oauth.OAuthToken.from_string(request_token)
    
    # If the token from session and token from twitter does not match                                                                                
    #   means something bad happened to tokens                                                                                                       
    if token.key != request.GET.get('oauth_token', 'no-token'):
        del request.session['request_token']
        # Redirect the user to the login page                                                                                                        
        return HttpResponse("Something wrong! Tokens do not match...")

    twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    try:
        access_token = twitter.fetch_access_token(token, oauth_verifier)
    except URLError:
        messages.error(request, 'Problem with connect to Twitter. Try again.')
        return redirect('auth:login')

    request.session['access_token'] = access_token.to_string()
    user = authenticate(access_token=access_token)

    # if user is authenticated then login user                                                                                                       
    if user:
        auth_login(request, user)
    else:
        # We were not able to authenticate user                                                                                                      
        # Redirect to login page                                                                                                                     
        del request.session['access_token']
        del request.session['request_token']
        return HttpResponseRedirect(reverse('auth:login'))

#    print('authenticated: {0}'.format(user.is_authenticated()))                                                                                     

    # authentication was successful, use is now logged in
    return HttpResponseRedirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))

@render_json
def maybe_logged_in(request):
    if request.user.is_authenticated():
        return { 'response': 'ok' }
    else:
        return { 'response': 'not_logged_in' }
