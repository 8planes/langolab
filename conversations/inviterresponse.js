if (typeof module == 'undefined') {
    goog.provide('ll.InviterResponse');
}

/**
 *
 * @enum {string}
 */
var InviterResponse = {
    MATCH: 'match',
    CONFLICT: 'conflict',
    NONE: 'none',
    ZERO_USERS: 'zerousers'
};

if (typeof module != 'undefined') {
    module.exports = exports = InviterResponse;
}
else {
    ll.InviterResponse = InviterResponse;
}