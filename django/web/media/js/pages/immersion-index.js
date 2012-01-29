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
    $('#interest_form').ajaxForm({
        dataType: 'json',
        success: function(data, status, xhr, $form) {
            if (data.success){
                $form.resetForm();
                $form.parent().hide().next().fadeIn();
            } else {
                for (key in data.errors) {
                    var ul = $('#' + key + '_errors');
                    ul.html(['<li>', data.errors[key], '</li>'].join(''));
                    ul.fadeIn();
                }
            }
        },
        beforeSubmit: function(formData, $form, options) {
            $('ul.errorlist', $form).hide();
        }
    });
    $('.pointslist a').click(function(e) {
        e.preventDefault();
        var largeImageName = $(this).attr("data-largeimage")
        window.pageTracker._trackPageview(largeImageName);
        var imageURL = IMAGES_DIR + largeImageName;
        $.nyroModalManual({
            url: imageURL
        });
        return false;
    });
    function preloadImage(index, image) {
        var img = new Image();
        img.src = IMAGES_DIR + image;
    }
    $.each(['interaction_large.png', 
            'interactionnotes_large.png', 
            'dashboard_large.jpg'],
           preloadImage);
    if ($.cookie("showHint") != "false")
        $('.hintDialog').delay(2000).fadeIn();
    $('.hintDialog a').click(function(e) {
        $.cookie("showHint", "false", { expires: 60 });
        e.preventDefault();
        $('.hintDialog').fadeOut();
        return false;
    });
});