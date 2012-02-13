var ConversationStat = require('../models/conversationstat');

function ensureUser(req, res, next) {
    if (req.user) {
        next();
    }
    else {
        res.redirect('/login?next=' + encodeURIComponent(req.url))
    }
}

module.exports = function(app) {
    app.get('/', function(req, res) {
        ConversationStat.topForLastWeek(5, function(stats) {
            res.render('index', {
                conversationStats: stats
            });
        });
    });
    app.get('/login', function(req, res) {
        res.render('login');
    });
    app.get('/enter_conversations', ensureUser, function(req, res) {
        
    });
};