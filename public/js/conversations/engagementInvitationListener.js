goog.provide('EngagementInvitationListener');

/**
 * @constructor
 */
EngagementInvitationListener = function(socket) {
};
goog.addSingletonGetter(EngagementInvitationListener);

EngagementInvitationListener.prototype.listen = function(socket, listener) {
    if (this.socket_) {
        throw new Exception();
    }
    this.socket_ = socket;
    this.listener_ = listener;
    this.socket_.on(
        'engagementInvitation',
        goog.bind(this.engagementInvitationReceived_, this));
};