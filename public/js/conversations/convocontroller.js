goog.provide('ll.ConvoController');

goog.require('ll.WaitingController');
goog.require('ll.MatchController');

ll.ConvoController.SOCKET_ = goog.global['SOCKET'];
ll.ConvoController.USER_ID_ = goog.global['USER_ID'];
ll.ConvoController.LANGUAGE_PAIRS_ = goog.global['LANGUAGE_PAIRS'];

ll.ConvoController.startWaiting_ = function() {
    if (ll.MatchController.getInstance().inMatch()) {
        return;
    }
    ll.WaitingController.getInstance().start(
        ll.ConvoController.SOCKET_,
        ll.ConvoController.USER_ID_,
        ll.ConvoController.LANGUAGE_PAIRS_);
};

ll.ConvoController.startMatch_ = function(matchID) {
    ll.MatchController.getInstance().start(
        matchID,
        ll.ConvoController.SOCKET_,
        ll.ConvoController.USER_ID_,
        ll.ConvoController.LANGUAGE_PAIRS_);
};

ll.ConvoController.SOCKET_['emit'](
    'setUserInfo', 
    ll.ConvoController.USER_ID_, 
    ll.ConvoController.LANGUAGE_PAIRS_,
    function(response) {
        var matchID = response['matchID'];
        if (goog.isNull(matchID)) {
            ll.ConvoController.startWaiting_();
        }
        else {
            ll.ConvoController.startMatch_(matchID);
        }
    });

ll.ConvoController.SOCKET_['on'](
    'matchStarted', 
    function(matchID) {
        ll.ConvoController.getInstance().startMatch_(matchID);
    });
