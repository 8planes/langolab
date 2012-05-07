goog.provide('ll.MatchController');

/**
 * @constructor
 */
ll.MatchController = function() {
};
goog.addSingletonGetter(ll.MatchController);

ll.MatchController.prototype.start = function(
    matchID, socket, userID, languagePairs) 
{
    this.matchID_ = matchID;
    this.socket_ = socket;
    this.userID_ = userID;
    this.languagePairs_ = languagePairs;
    
};

