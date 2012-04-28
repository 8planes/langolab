var decorators = require('./decorators'),
ConversationStat = require('../models/conversationstat'),
User = require('../models/user'),
WaitingUser = require('../models/waitinguser'),
_und = require('underscore'),
settings = require('../settings'),
socketio = require('socket.io'),
pubsub = require('../singletonpubsub');

function updateConversationStats(user) {
    var date = new Date();
    var languagePairs = user.languagePairs();
    _und.each(languagePairs, function(lp) {
        ConversationStat.increment(lp[0], lp[1], date);
    });
}

function waitingChannel(userID) {
    return userID + "_waiting";
}

function socketStarted(socket, userID, languagePairs) {
    socket.on('disconnect', function() {
        stopWaiting(socket, userID);
    });
    WaitingUser.nextAvailableUser(
        languagePairs,
        function(matchedUser) {
            if (matchedUser) {
                stopWaiting(socket, userID);
                startMatch(socket, userID, matchedUser._id);
            }
            else {
                startWaiting(socket, userID, languagePairs);
            }
        });
}

function startMatch(socket, userID, matchedUserID) {
    var match = new Match();
    match.user0 = mongoose.Type.ObjectId(userID);
    match.user1 = matchedUserID;
    match.dateStarted = new Date();
    match.save(function(err) {
        socket.emit("matchStarted", match._id + '');
        pubsub.publish(
            waitingChannel(matchedUserID + ''),
            match._id + '');
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
            socket.emit("matchStarted", matchID);
        });
    WaitingUser.start(
        mongoose.Types.ObjectId(userID),
        languagePairs,
        function() {});
}

module.exports = function(app, io) {
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
            socketStarted(socket, userID, languagePairs);
            callback("okay");
        });
    });
};
