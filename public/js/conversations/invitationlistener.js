goog.provide('ll.InvitationListener');

/**
 * @constructor
 */
ll.InvitationListener = function() {
};
goog.addSingletonGetter(ll.InvitationListener);

ll.InvitationListener.prototype.listen = function(socket, listener) {
    if (this.socket_) {
        throw new Exception();
    }
    this.socket_ = socket;
    this.listener_ = listener;
    this.socket_['on'](
        'engagementInvitation',
        goog.bind(this.invitationReceived_, this));
};

ll.InvitationListener.prototype.invitationReceived_ = function() {
    console.log(arguments);
};
