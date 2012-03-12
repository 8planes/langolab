var pubsub = require('../singletonpubsub.js'),
WaitingUser = require('../models/waitinguser.js'),
_und = require('underscore'),
InviterResponse = require('./inviterresponse.js');

var PING_THRESHOLD = 8;

var InviterController = function(userID) {
    /**
     * @type {ObjectId}
     */
    this.userID_ = userID;
}

/**
 * @param {Array.<Array.<string>>} languagePairs
 * @param {function(InviterResponse)} callback
 */
InviterController.prototype.makeInvitations = 
    function(languagePairs, callback) 
{
    console.log("makeInvitations");
    this.callback_ = callback;
    var userList = [];
    var numQueriesExecuted = 0;
    var pingTimeout = new Date(new Date().getTime() - PING_THRESHOLD * 1000);
    var that = this;
    _und.each(
        languagePairs,
        function(lp) {
            WaitingUser
                .where('languages').elemMatch({
                    foreignLanguage: lp[0],
                    nativeLanguage: lp[1]
                })
                .where('lastPing').gte(pingTimeout)
                .run(function(err, results) {
                    userList.concat(results);
                    numQueriesExecuted++;
                    if (numQueriesExecuted == languagePairs.length) {
                        that.processAndInviteUserList_(userList);
                    }
                });
        });
};

InviterController.prototype.processAndInviteUserList_ = 
    function(rawUserList) 
{
    if (rawUserList.length == 0) {
        this.callback_(InviterResponse.ZERO_USERS);
        return;
    }
    rawUserList = _und.sortBy(
        rawUserList,
        function(user) { return user.userID; });
    rawUserList = _und.uniq(
        rawUserList, true, 
        function(user) { return user.userID; });
    // see http://www.mongodb.org/display/DOCS/Optimizing+Object+IDs#OptimizingObjectIDs-Sortbyidtosortbyinsertiontime
    rawUserList = _und.sortBy(
        rawUserList,
        function(user) { return user._id; });
    this.inviteUserList_(rawUserList);
};

InviterController.prototype.inviteUserList_ = function(userIDList) {
    console.log("inviteUserList_");
    console.log(userIDList);
    var that = this;
    var accepted = false;
    var numResponses = 0;
    var atLeastOneConflict = false;
    this.iterateUsers_(userIDList, function(userID) {
        that.inviteUser_(userID, function(response, invitedCallback) {
            numResponses++;
            if (response == InviteeResponse.CONFLICT) {
                atLeastOneConflict = true;
            }
            else if (response == InviteeResponse.ACCEPTED) {
                if (!accepted) {
                    invitedCallback(true);
                    accepted = true;
                    that.callback_(InviterResponse.MATCH);
                }
                else {
                    invitedCallback(false);
                }
            }
            if (numResponses == userIDList.length && !accepted) {
                if (atLeastOneConflict) {
                    that.callback_(InviterResponse.CONFLICT);
                }
                else {
                    that.callback_(InviterResponse.NONE);
                }
            }
        });
    });
};

InviterController.prototype.iterateUsers_ = 
    function(userList, fn, opt_curIndex) 
{
    var curIndex = opt_curIndex || 0;
    fn(userList[curIndex].userID);
    setTimeout(
        _und.bind(this.iterateUsers_, this, userList, fn, curIndex + 1),
        250);
};

/**
 * @param {ObjectId} userID
 * @param {function(InviteeResponse, function(boolean)=)} callback 
 *     Called to indicate whether the invited user got the slot or
 *     not.
 */
InviterController.prototype.inviteUser_ = function(userID, callback) {
    var token = [this.userID_.toString(), userID.toString()].join(':');
    var timedOut = false;
    pubsub.publish(inviteChannel(userID), token);
    var confirm = function(accepted) {
        pubsub.publish(invitationConfirmationChannel(token), accepted);
    };
    pubsub.subscribe(invitationResponseChannel(token),
        function(inviteeResponse) {
            if (timedOut) {
                confirm(false);
            }
            else {
                callback(inviteeReponse, confirm);
            }
        });
    setTimeout(
        function() {
            timedOut = true;
            pubsub.unsubscribe(invitationResponseChannel(token));
            callback(InviteeResponse.TIMEOUT);
        },
        5000);
};

module.exports = exports = InviterController;
