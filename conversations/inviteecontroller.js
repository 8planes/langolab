var pubsub = require('../singletonpubsub.js'),
channels = require('./channels.js'),
_und = require('underscore');

/**
 * @constructor
 */
var InviteeController = function(userID, socket) {
    this.userID_ = userID;
    this.socket_ = socket;
};

InviteeController.prototype.listenForInvitations = function() {
    pubsub.subscribe(
        channels.inviteChannel(this.userID_),
        _und.bind(this.invitationReceived_, this));
};

InviteeController.prototype.invitationReceived_ = function(token) {
    this.socket_.emit("invitationReceived", { token: token });
};

InviteeController.prototype.invitationResponseReceived = function(data) {
    var that = this;
    pubsub.publish(
        channels.invitationResponseChannel(data.token), 
        data.response);
    if (data.response == InviteeResponse.ACCEPTED) {
        var confirmationChannel = 
            channels.invitationConfirmationChannel(data.token);
        var unsubscribe = function() {
            pubsub.unsubscribe(confirmationChannel);
        };
        pubsub.subscribe(
            confirmationChannel,
            function(accepted) {
                that.invitationConfirmationReceived_(data.token, accepted);
                unsubscribe();
            });
        setTimeout(unsubscribe, 4000);
    }
};

InviteeController.prototype.invitationConfirmationReceived_ = 
    function(token, accepted) 
{
    this.socket_.emit(
        "invitationConfirmation",
        { token: token,
          accepted: accepted });
};

module.exports = exports = InviteeController;