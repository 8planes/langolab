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

var empty_form = $('.empty-form').html();
var $form_count_field = $('#id_preferreduserlanguage_set-TOTAL_FORMS')

// fix saving value by browser after refresh
$('.delete-checkbox input').attr('checked', false); 
$form_count_field.val(form_count);

$('.language_list .remove-language').live('click', function() {
    $(this).parent().slideUp().find('.delete-checkbox input').attr('checked', true);
    return false;
});

$('.add-language').click(function(){
    form_count++;
    $form_count_field.val(form_count);
    var form = $(empty_form.replace(/__prefix__/g, form_count - 1 + ''));
    form.hide();
    $('.language_list li:last').after(form);
    form.slideDown();
    return false;
});

function languagesValidate() {
    var valid = true;
    $('.language_list .user_language').each(function() {
        if (!valid) return;
        if ($(this).css('display') != 'none') {
            $(this).children('select').each(function() {
                if (!valid) return;
                if (!$(this).val()) {
                    alert('Not all languages are completely specified');
                    valid = false;
                }
            });
        }
    });
    return valid;
}

function languagesSubmit(opt_callback) {
    $('#user_language_form').ajaxSubmit(opt_callback);
}
