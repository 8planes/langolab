var decorators = require('./decorators'),
ConversationStat = require('../models/conversationstat'),
User = require('../models/user'),
WaitingUser = require('../models/waitinguser'),
_und = require('underscore'),
settings = require('../settings'),
socketio = require('socket.io'),
InviteeController = require('../conversations/inviteecontroller.js'),
InviterController = require('../conversations/invitercontroller.js');

function updateConversationStats(user) {
    var date = new Date();
    var languagePairs = user.languagePairs();
    _und.each(languagePairs, function(lp) {
        ConversationStat.increment(lp[0], lp[1], date);
    });
}

function addMakeInvitationListener(socket, userID) {
    console.log("Adding makeInvitationsListener");
    socket.on(
        'makeInvitations',
        function(languagePairs, callback) {
            console.log("makeInvitations called");
            var inviterController = new InviterController(userID);
            inviterController.makeInvitations(
                languagePairs, callback);
        });
}

function addReceiveInvitationListener(socket, userID) {
    var inviteeController = new InviteeController(userID);
    inviteeController.listenForInvitations(socket);
    socket.on(
        "invitationResponse",
        _und.bind(
            inviteeController.invitationResponseReceived, 
            inviteeController));
}

function socketStarted(socket, userID, languagePairs) {
    WaitingUser.ping(userID, languagePairs, function() {
        addMakeInvitationListener(socket, userID);
        addReceiveInvitationListener(socket, userID);
    });
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
    // doing this because of http://devcenter.heroku.com/articles/using-socket-io-with-node-js-on-heroku
    // :(
    var io = socketio.listen(app);
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
