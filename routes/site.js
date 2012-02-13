var ConversationStat = require('../models/conversationstat');

module.exports = function(app) {
    app.get('/', function(req, res) {
        ConversationStat.topForLastWeek(5, function(stats) {
            res.render('index', {
                conversationStats: stats
            });
        });
    });
};