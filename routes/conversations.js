var decorators = require('./decorators'),
ConversationStat = require('../models/conversationstat'),
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
    socket.on(
        'makeInvitations',
        function(token, languagePairs) {
            var invitaterController = new InviterController(userID);
            inviterController.makeInvitations(
                languagePairs, function(inviterResponse) {
                    socket.emit(
                        'makeInvitationsReply', 
                        { token: token,
                          response: inviterResponse });
                });
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

function socketStarted(socket, userID) {
    // TODO: add WaitingUser record.
    addMakeInvitationListener(socket, userID);
    addReceiveInvitationListener(socket, userID);
    // TODO: listen for disconnect.
}

module.exports = function(app, io) {
    app.get(
        '/conversations', decorators.ensureUserLanguages,
        function(req, res) {
            updateConversationStats(req.user);
            res.render('conversations');
        });
    var io = socketio.listen(app);
    io.sockets.on('connection', function(socket) {
        socket.on('setUserID', function(userID) {
            socketStarted(socket, userID);
        });
    });
};
