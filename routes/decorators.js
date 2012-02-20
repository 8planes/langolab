function ensureUser(req, res, next) {
    if (req.isAuthenticated()) {
        next();
    }
    else {
        res.redirect('/login?next=' + encodeURIComponent(req.url))
    }
}

exports.ensureUser = ensureUser;

exports.ensureUserLanguages = function(req, res, next) {
    ensureUser(req, res, function() {
        if (req.user.nativeLanguages.length > 0 &&
            req.user.foreignLanguages.length > 0) {
            next();
        }
        else {
            res.redirect('/enterConversations')
        }
    });
    
}