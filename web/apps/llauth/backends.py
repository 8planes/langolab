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

import sys
from llauth.models import CustomUser as User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
import facebook
from socialauth.lib import oauthtwitter
from socialauth.models import OpenidProfile as UserAssociation, FacebookUserProfile, TwitterUserProfile, AuthMeta
import urllib
from datetime import datetime
import random
from django.contrib.auth.backends import ModelBackend

TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')
FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

class CustomUserBackend(ModelBackend):    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username, is_active=True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class OpenIdBackend:
    def authenticate(self, openid_key, request, provider):
        try:
            assoc = UserAssociation.objects.get(openid_key=openid_key)
            if assoc.user.is_active:
                return assoc.user
            else:
                return
        except UserAssociation.DoesNotExist:
            #fetch if openid provider provides any simple registration fields
            nickname = None
            email = None
            if request.openid and request.openid.sreg:
                email = request.openid.sreg.get('email')
                nickname = request.openid.sreg.get('nickname')
            elif request.openid and request.openid.ax:
                if provider in ('Google', 'Yahoo'):
                    email = request.openid.ax.get('http://axschema.org/contact/email')
                    email = email.pop()
                else:
                    email = request.openid.ax.get('email')                      
                    nickname = request.openid.ax.get('nickname')

            if nickname is None :
                if email:
                    nickname = email.split('@')[0]
                else:
                    nickname =  ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(10)])
            if email is None :
                valid_username = False
                email =  None #'%s@example.openid.com'%(nickname)
            else:
                valid_username = True
            name_count = User.objects.filter(username__startswith = nickname).count()

            if name_count:
                username = '%s%s'%(nickname, name_count + 1)
                user = User.objects.create_user(username,email or '')
            else:
                user = User.objects.create_user(nickname,email or '')
            user.save()

            #create openid association
            assoc = UserAssociation()
            assoc.openid_key = openid_key
            assoc.user = user#AuthUser.objects.get(pk=user.pk)
            if email:
                assoc.email = email
            if nickname:
                assoc.nickname = nickname
            if valid_username:
                assoc.is_username_valid = True
            assoc.save()

            #Create AuthMeta
            auth_meta = AuthMeta(user = user, provider = provider)
            auth_meta.save()
            return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id)
            return user
        except User.DoesNotExist:
            return None


class FacebookBackend:
    def authenticate(self, request, user=None):
        cookie = facebook.get_user_from_cookie(request.COOKIES,
                                               FACEBOOK_APP_ID,
                                               FACEBOOK_SECRET_KEY)

        if cookie:
            uid = cookie['uid']
            access_token = cookie['access_token']
        else:
            # if cookie does not exist
            # assume logging in normal way
            params = {}
            params["client_id"] = FACEBOOK_APP_ID
            params["client_secret"] = FACEBOOK_SECRET_KEY
            params["redirect_uri"] = '%s://%s%s' % (
                         'https' if request.is_secure() else 'http',
                         Site.objects.get_current().domain,
                         reverse("socialauth_facebook_login_done"))
            params["code"] = request.GET.get('code', '')

            url = ("https://graph.facebook.com/oauth/access_token?"
                   + urllib.urlencode(params))
            from cgi import parse_qs
            userdata = urllib.urlopen(url).read()
            res_parse_qs = parse_qs(userdata)
            # Could be a bot query
            if not res_parse_qs.has_key('access_token'):
                return None
                
            access_token = res_parse_qs['access_token'][-1]
            
            graph = facebook.GraphAPI(access_token)
            uid = graph.get_object('me')['id']
            
        try:
            fb_user = FacebookUserProfile.objects.get(facebook_uid=uid)
            return fb_user.user

        except FacebookUserProfile.DoesNotExist:

            # create new FacebookUserProfile
            graph = facebook.GraphAPI(access_token) 
            fb_data = graph.get_object("me")

            if not fb_data:
                return None

            username = uid
            if not user:
                user = User.objects.create(username=username)
                if 'email' in fb_data:
                    user.email = fb_data['email']
                user.first_name = fb_data['first_name']
                user.last_name = fb_data['last_name']
                user.profile_photo_url = \
                    'http://graph.facebook.com/{0}/picture'.format(uid)
                user.nickname = str(user)
                user.save()
                
            fb_profile = FacebookUserProfile(facebook_uid=uid, user=user)
            fb_profile.save()
            
            auth_meta = AuthMeta(user=user, provider='Facebook').save()
                
            return user

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

from urllib import urlopen
from django.core.files.base import ContentFile

class TwitterBackend:
    """TwitterBackend for authentication                                                                                                                 
    """
    def authenticate(self, access_token):
        '''authenticates the token by requesting user information from twitter                                                                           
        '''
        twitter = oauthtwitter.OAuthApi(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, access_token)

        try:
            userinfo = twitter.GetUserInfo()
        except:
            # If we cannot get the user information, user cannot be authenticated                                                                        
            raise

        screen_name = userinfo.screen_name
        img_url = userinfo.profile_image_url

        try:
            user_profile = TwitterUserProfile.objects.get(screen_name = screen_name)
            if user_profile.user.is_active:
                return user_profile.user
            else:
                return
        except TwitterUserProfile.DoesNotExist:
            #Create new user                                                                                                                             
            same_name_count = User.objects.filter(username__startswith = screen_name).count()
            if same_name_count:
                username = '%s%s' % (screen_name, same_name_count + 1)
            else:
                username = screen_name
            username = '@'+username

            name_count = User.objects.filter(username__startswith = username).count()

            if name_count:
                username = '%s%s'%(username, name_count + 1)

            user = User(username =  username)
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)
            name_data = userinfo.name.split()
            try:
                first_name, last_name = name_data[0], ' '.join(name_data[1:])
            except:
                first_name, last_name =  screen_name, ''
            user.first_name, user.last_name = first_name, last_name
            #user.email = '%s@twitteruser.%s.com'%(userinfo.screen_name, settings.SITE_NAME)                                                             
            user.save()
            userprofile = TwitterUserProfile(user = user, screen_name = screen_name)
            userprofile.access_token = access_token.key
            userprofile.url = userinfo.url
            userprofile.location = userinfo.location
            userprofile.description = userinfo.description
            userprofile.profile_image_url = userinfo.profile_image_url
            userprofile.save()
            AuthMeta(user=user, provider='Twitter').save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
