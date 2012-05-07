var decorators = require('./decorators'),
WeeklyStat = require('../models/weeklystat'),
User = require('../models/user'),
WaitingUser = require('../models/waitinguser'),
_und = require('underscore'),
settings = require('../settings'),
socketio = require('socket.io'),
pubsub = require('../singletonpubsub');

function updateConversationStats(user) {
    var languagePairs = user.languagePairs();
    _und.each(languagePairs, function(lp) {
        WeeklyStat.increment(lp[0], lp[1]);
        HourlyStat.increment(lp[0], lp[1]);
    });
}

function waitingChannel(userID) {
    return userID.toString() + "_waiting";
}

function socketStarted(socket, userID, languagePairs, callback) {
    socket.on('disconnect', function() {
        stopWaiting(socket, userID);
    });
    WaitingUser.nextAvailableUser(
        languagePairs,
        function(matchedUser) {
            if (matchedUser) {
                stopWaiting(socket, userID);
                startMatch(socket, userID, matchedUser._id, callback);
            }
            else {
                startWaiting(socket, userID, languagePairs);
                callback(null);
            }
        });
}

function startMatch(socket, userID, matchedUserID, callback) {
    Match.start(userID, matchedUserID, function(match) {
        callback(match._id.toString());
        pubsub.publish(
            waitingChannel(matchedUserID),
            match._id.toString());
    });
}

function stopWaiting(socket, userID) {
    WaitingUser.stop(userID);
    pubsub.unsubscribe(waitingChannel(userID));
}

function startWaiting(socket, userID, languagePairs) {
    pubsub.subscribe(
        waitingChannel(userID),
        function(matchID) {
            stopWaiting(socket, userID);
            socket.emit("matchStarted", String(matchID));
        });
    WaitingUser.start(
        userID, languagePairs, function() {});
}

function addMockups(app) {
    app.get(
        "/waitingmockup", 
        function(req, res) {
            res.render('waitingmockup');
        });
}

module.exports = function(app, io) {
    addMockups(app);
    app.get(
        '/conversations', decorators.ensureUserLanguages,
        function(req, res) {
            updateConversationStats(req.user);
            res.render(
                'conversations',
                { "userID": req.user.id,
                  "languagePairs": JSON.stringify(
                      req.user.languagePairs()) });
        });
    var io = socketio.listen(app);
    // doing this because of http://devcenter.heroku.com/articles/using-socket-io-with-node-js-on-heroku
    // :(
    io.configure(function() {
        io.set("transports", ["xhr-polling"]); 
        io.set("polling duration", 10);
    });
    io.sockets.on('connection', function(socket) {
        socket.on('setUserInfo', function(userID, languagePairs, callback) {
            socketStarted(
                socket, userID, languagePairs, 
                function(matchID) {
                    callback(JSON.stringify({ "matchID": matchID }));
                });
        });
    });
};
