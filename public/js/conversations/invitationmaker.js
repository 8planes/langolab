goog.provide('ll.InvitationMaker');

/**
 * @constructor
 */
ll.InvitationMaker = function() {
};
goog.addSingletonGetter(ll.InvitationMaker);


/**
 * @param {Object} socket
 * @param {function(ll.WaitingRoutine.InviterResponse)} callback
 */
ll.InvitationMaker.prototype.attemptToEngage = function(socket, callback) {
    socket['emit'](
        'makeInvitations',
        [['en', 'es'], ['en', 'de']],
        callback);
};
