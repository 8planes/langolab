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

jQuery(function($) {
    $('.facebook').click(login(popupType.FACEBOOK));
    $('.google').click(login(popupType.GOOGLE));
    $('.twitter').click(login(popupType.TWITTER));
});

function randomString() {
    var sb = [], i;
    for (i = 0; i < 10; i++)
        sb.push((10 + ~~(Math.random() * 26)).toString(36));
    return sb.join('') + (new Date().getTime() % 100000000);
};

var popupType = {
    FACEBOOK: [
        '/socialauth/facebook_login/',
        'location=0,status=0,width=800,height=400'
    ],
    TWITTER: [
        '/llauth/twitter_login/',
        'location=0,status=0,width=800,height=400'
    ],
    GOOGLE: [
        '/socialauth/gmail_login/?next=/conversations/determine_languages/',
        'location=0,status=0,width=800,height=400'
    ]
};

function maybeLoggedIn(callback) {
    jQuery.getJSON(
        '/llauth/maybe_logged_in/',
        function(data) {
            if (data.response == 'ok')
                window.location = '/conversations/waiting_list/';
        });
}

function openLoginPopup(type, callback) {
    var loginWin = window.open(
        type[0], randomString(), type[1]);
    var timer = {};
    timer.intervalID = window.setInterval(
        function() {
            if (loginWin.closed) {
                window.clearInterval(timer.intervalID);
                maybeLoggedIn(callback);
            }
        }, 250);
}

function login(type) {
    return function() {
        openLoginPopup(type);
        return false;
    };
}
