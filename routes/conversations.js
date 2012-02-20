var decorators = require('./decorators'),
ConversationStat = require('../models/conversationstat'),
_und = require('underscore');

function updateConversationStats(user) {
    var date = new Date();
    var languagePairs = user.languagePairs();
    _und.each(languagePairs, function(lp) {
        ConversationStat.increment(lp[0], lp[1], date);
    });
}

module.exports = function(app) {
    app.get(
        '/conversations', decorators.ensureUserLanguages,
        function(req, res) {
            updateConversationStats(req.user);
            res.render('conversations');
        });
};
