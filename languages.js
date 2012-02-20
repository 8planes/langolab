var _und = require("underscore");

var languages = [
    ['en', 'English'],
    ['es', 'Spanish'],
    ['de', 'German']];
var languageMap = {};
_und.each(languages,
          function(lp) {
              languageMap[lp[0]] = lp[1];
          });

exports.LANGUAGES = languages;
exports.LANGUAGE_MAP = languageMap;
