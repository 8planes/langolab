(function() {
    function addLanguageSelect(type) {
        var div = $('<div/>').addClass(type + '-language');
        var selector = $('<select/>');
        div.append(selector);
        _.each(
            LANGUAGES,
            function(l) {
                selector.append($('<option/>').attr(
                    'value', l[0]).text(l[1]));
            });
        div.append($('<a/>').addClass('remove').attr(
            'href', 'javascript:void(0)').text('Remove'));
        $('div.' + type + '-languages').append(div);
    }

    function removeLanguage(e) {
        e.preventDefault();
        $(this).parent().remove();
    }

    function addNativeLanguage(e) {
        e.preventDefault();
        addLanguageSelect('native');
    }

    function addForeignLanguage(e) {
        e.preventDefault();
        addLanguageSelect('foreign');
    }

    function getLanguages(type) {
        var selects = $('div.' + type + '-languages select');
        var languages = [];
        selects.each(function() {
            languages.push($(this).val());
        });
        return languages;
    }

    function continueToConversation(e) {
        e.preventDefault();
        var nativeLanguages = getLanguages('native');
        var foreignLanguages = getLanguages('foreign');
        if (nativeLanguages.length == 0 || 
            foreignLanguages.length == 0) {
            alert("You have to select at least native langauge and one foreign.");
            return;
        }
        $.getJSON(
            'languagesKnown', 
            { 'foreignLanguages': foreignLanguages.join(','),
              'nativeLanguages': nativeLanguages.join(',') }, 
            function(response) {
                if (response.success) {
                    window.location.href = "/conversations";
                }
            });
    };

    $(function() {
        $('div.native a.add').click(addNativeLanguage);
        $('div.foreign a.add').click(addForeignLanguage);
        $('.native-language a.remove, .foreign-language a.remove').live(
            'click', removeLanguage);
        $('a.continue').click(continueToConversation);
    });
})();
