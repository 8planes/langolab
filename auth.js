var _und = require('underscore'),
passport = require('passport'),
settings = require('./settings'),
User = require('./models/user'),
LocalStrategy = require('passport-local').Strategy,
FacebookStrategy = require('passport-facebook').Strategy,
TwitterStrategy = require('passport-twitter').Strategy,
GoogleStrategy = require('passport-google').Strategy;

passport.serializeUser(function(user, done) {
    done(null, user.id);
});

passport.deserializeUser(function(id, done) {
    User.findById(id, function(err, user) {
        if (err) {
            done(new Error("User " + id + " does not exist."));
        }
        else {
            done(null, user);
        }
    });
});

passport.use(new LocalStrategy(
    { usernameField: 'login-username',
      passwordField: 'login-password' },
    function(username, password, done) {
        console.log('local strat in effect, yall');
        User.findOne(
            { 'name': username },
            function(err, doc) {
                if (err) {
                    done(err);
                }
                else if (!doc) {
                    done(null, false);
                }
                else {
                    doc.authenticate(
                        password,
                        function(err, res) {
                            done(null, res ? doc : false);
                        });
                }
            });
    }));

function incrementUsername(name) {
    var match = /(\d+)$/g.exec(name);
    if (!match) {
        return name + "0";
    }
    else {
        return name + (parseInt(match[1]) + 1);
    }
};

function assignUsername(user, preferredNames, callback) {
    // note that a race condition could still result in a 
    // duplicate name here. one way to avoid this would be 
    // to reserve names in a separate collection.
    // The race condition is highly unlikely without a ton
    // of users, or possibly ever.
    User.findOne(
        { 'name': preferredNames[0] },
        function(err, doc) {
            if (err) {
                callback(err);
            }
            else if (!doc) {
                user.name = preferredNames[0];
                callback();
            }
            else {
                // username taken :(
                var newName = incrementUsername(preferredNames[0]);
                preferredNames.splice(0, 1);
                preferredNames.push(newName);
                assignUsername(user, preferredNames, callback);
            }
        });
};

function createFacebookUser(profile, done) {
    var user = new User();
    assignUsername(user, [profile.displayName, profile.username], function(err) {
        if (err) {
            done(err);
        }
        else {
            console.log(profile);
            user.fb = {
                username: profile.username,
                displayName: profile.displayName,
                lastName: profile.name.familyName,
                firstName: profile.name.givenName,
                middleName: profile.name.middleName,
                gender: profile.gender,
                profileURL: profile.profileURL
            };
            if (user.fb.emails.length > 0) {
                user.email = user.fb.emails[0];
            }
            user.save(function(err) {
                if (err) {
                    done(err);
                }
                else {
                    done(null, user);
                }
            });
        }
    });
};

passport.use(new FacebookStrategy(
    {
        clientID: settings.FACEBOOK_APP_ID,
        clientSecret: settings.FACEBOOK_APP_SECRET,
        callbackURL: settings.BASE_URL + "/facebook_callback" 
    },
    function(accessToken, refreshToken, profile, done) {
        // for profile schema see https://github.com/jaredhanson/passport-facebook/blob/master/lib/passport-facebook/strategy.js
        user = User.findOne(
            { 'fb.id': profile.id },
            function(err, doc) {
                if (err) {
                    done(err);
                }
                else if (!doc) {
                    createFacebookUser(profile, done);
                }
                else {
                    done(null, doc);
                }
            });
    }));

exports.assignUsername = assignUsername;