/*
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
*/

function facebookURL(message) {
    var description = "Help us turn Langolab into the best place on the web to meet and chat with foreign language speakers over webcam!";
    return 'http://www.facebook.com/dialog/feed' +
        '?app_id=' + FACEBOOK_APP_ID + 
        '&link=' + encodeURIComponent('http://www.langolab.com') +
        '&picture=' + encodeURIComponent(FB_IMAGE) +
        '&display=popup' +
        '&message=' + encodeURIComponent(message) +
        '&description=' + encodeURIComponent(description) +
        '&redirect_uri=' + encodeURIComponent(POPUP_REDIRECT_URL);
}

function openFacebook(message) {
    window.open(
        facebookURL(message),
        'post_to_fb', 'status=0,width=580,height=400');
}

function openTwitter(msg) {
    var url = "http://twitter.com/share?text=" + encodeURIComponent(msg) +
        "&url=" + encodeURIComponent('http://www.langolab.com');
    window.open(
        url,
        'post_to_tw', 'status=0,width=580,height=400');
}

function getFBSiteMessage() {
    return "Visit Langolab to practice a foreign language with a native speaker, live over webcam! It's like chatroulette for language learning. #langolab"
}

function getTWSiteMessage() {
    return "Visit Langolab to practice a foreign language with a native speaker, live over webcam! Like chatroulette for languages."
}

$(function() {
    $('a.fb-sharesite').click(function(e) {
        e.preventDefault();
        openFacebook(getFBSiteMessage());
    });
    $('a.tw-sharesite').click(function(e) {
        e.preventDefault();
        openTwitter(getTWSiteMessage());
    });
});