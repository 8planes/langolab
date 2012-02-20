/*
Langolab -- learn foreign languages by speaking with random native speakers over webcam.
Copyright (C) 2012 Adam Duston

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

$(function() {
    $('#creation_form button').click(function(e) {
        e.preventDefault();
        var url = $('#creation_form').attr('action');
        $.post(url,
               $('#creation_form').serialize(),
               function(data) {
                   if (data.success) {
                       window.location.href = './enterConversations';
                   }
                   else {
                       console.log(data.errors);
                   }
               },
               'json');
        return false;
    });
});