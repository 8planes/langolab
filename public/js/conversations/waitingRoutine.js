goog.provide("WaitingRoutine");

goog.require("goog.Timer");

/**
 * @constructor
 */
function WaitingRoutine(socket) {

};
goog.addSingletonGetter(WaitingRoutine);

/**
 * @param {function(string)} engagementCallback Called with room id
 *     when connected
 */
WaitingRoutine.prototype.start = function(socket, engagementCallback) {
    if (this.waiting_) {
        return;
    }
    this.waiting_ = true;
    this.socket_ = socket;
    this.engagementCallback_ = engagementCallback;
    this.invitationListener_ = EngagementInvitationListener.getInstance();
    this.invitationMaker_ = EngagementInvitationMaker.getInstance();
    this.invitationListener_.listen(
        socket, 
        goog.bind(this.invitationReceived_, this));
    this.attemptToEngage_();
};

WaitingRoutine.prototype.attemptToEngage_ = function() {
    this.attemptingToEngage_ = true;
    this.invitationMaker_.attemptToEngage(
        this.socket_,
        goog.bind(this.engagementAttemptReturned_, this));
};

WaitingRoutine.prototype.engagementAttemptReturned_ = function(result) {
    this.attemptingToEngage_ = false;
    if (result['none']) {
        // no results. we're waiting.
        this.startHeartbeat_();
    }
    else if (result['match']) {
        // we're matched!
        this.stopWaiting_();
        this.invitationListener_.stop();
        this.engagementCallback_(result['roomID']);
    }
    else {
        // there was a conflict. try again soon.
        this.startHeartbeat_();
        this.invitationListener_.stop();
        goog.Timer.callOnce(
            this.attemptToEngage_,
            3000 + Math.random() * 10000,
            this);
    }
};

WaitingRoutine.prototype.startHeartbeat_ = function() {
    // make and start this.heartbeatTimer_
};

WaitingRoutine.prototype.stopWaiting_ = function() {
    this.heartbeatTimer_.stop();
    this.invitationListener_.stop();
    this.waiting_ = false;
};

WaitingRoutine.prototype.invitationReceived_ = function(invitation) {
    if (!this.waiting_) {
        invitation.reject();
    }
    if (this.attemptingToEngage_ || this.respondingToInvitation_) {
        invitation.conflict();
    }
    else {
        this.respondingToInvitation_ = true;
        var that = this;
        invitation.accept(function(confirm) {
            that.respondingToInvitation_ = false;
            if (confirm) {
                // we're engaged!
                that.stopWaiting_();
                that.engagementCallback_(invitation.ROOM_ID);
            }
        });
    }
};
