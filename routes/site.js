var auth = require('../auth.js'),
passport = require('passport'),
check = require('validator').check,
_und = require('underscore'),
User = require('../models/user.js'),
languages = require('../languages.js'),
decorators = require('./decorators.js');

var WeeklyStat = require('../models/weeklystat');

/**
 * @param {Object} data POST data from create user form
 * @param {function(Object)} callback Function that takes errors
 *     map as argument. No errors if errors map has length of zero.
 */
function createUserErrors(data, callback) {
    var errors = {};
    try {
        check(data.email).len(6, 64).isEmail();
    }
    catch (e) {
        errors['email_error'] = "Invalid email address";
    }
    try {
        check(data.password).len(5, 128);
    }
    catch (e) {
        errors['password_error'] = "Password must be at least 5 characters";
    }
    User.findOne(
        { 'email': data.email },
        function(err, doc) {
            if (doc) {
                errors['email_duplicate'] = true;
            }
            callback(errors);
        });
}

/**
 * @param {Object} data POST from createAccount call.
 * @param {function(User)} callback
 */
function createUserImpl(data, callback) {
    var user = new User();
    auth.assignUsername(user, [data.username], function(err) {
        user.email = data.email;
        user.setPassword(data.password, function() {
            user.save(function(err) {
                // TODO: deal with possible error.
                callback(user);
            });
        });
    });
};

/**
 * @param {Object} data POST from createAccount call.
 * @param {function(User=, ?Object)} callback Callback with users and 
 *     errors Object.
 */
function createUser(data, callback) {
    createUserErrors(data, function(errors) {
        if (_und.size(errors) > 0) {
            callback(null, errors);
        }
        else {
            createUserImpl(data, function(user) {
                callback(user);
            });
        }
    });
}

module.exports = function(app) {
    app.get('/', function(req, res) {
        WeeklyStat.topForLastWeek(5, function(stats) {
            res.render('index', {
                conversationStats: stats
            });
        });
    });
    app.get('/login', function(req, res) {
        res.render('login', { nextURL: req.query.next || '/' });
    });
    app.post('/loginPost', 
             passport.authenticate('local'),
             function(req, res) {
                 console.log(req.isAuthenticated());
                 console.log(req.user);
                 if (req.isAuthenticated()) {
                     res.json({ success: true });
                 }
                 else {
                     res.json({ success: false, 
                                errors: { who_knows: true } });
                 }
             });
    app.post('/createUser', function(req, res) {
        var data = req.body;
        createUser(data, function(user, errors) {
            if (!user) {
                res.json({ success: false, errors: errors });
            }
            else {
                console.log("logging in!");
                req.logIn(user, function(err) {
                    res.json({ success: true });
                });
            }
        });
    });
    app.get('/enterConversations', decorators.ensureUser, function(req, res) {
        res.render(
            'enterConversations',
            { 'nativeLanguages': req.user.nativeLanguages,
              'foreignLanguages': req.user.foreignLanguages,
              'languages': languages.LANGUAGES,
              'languageJSON': JSON.stringify(languages.LANGUAGES) });
    });
    app.get('/languagesKnown', function(req, res) {
        var nativeLanguages = req.query.nativeLanguages.split(',');
        var foreignLanguages = req.query.foreignLanguages.split(',');
        User.update(
            { _id: req.user._id },
            { $set: {
                nativeLanguages: nativeLanguages,
                foreignLanguages: foreignLanguages
            }},
            {},
            function(err, numAffected) {
                res.json({ success: true });
            });
    });
};