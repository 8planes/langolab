/**
 *
 * @enum {string}
 */
var InviteeResponse = {
    TIMEOUT: 'timeout',
    CONFLICT: 'conflict',
    ACCEPTED: 'accepted',
    REJECTED: 'rejected'
};

if (module) {
    module.exports = exports = InviteeResponse;
}
