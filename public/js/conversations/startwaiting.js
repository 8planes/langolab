goog.provide('ll.StartWaiting');

goog.require('ll.WaitingRoutine');

var socket = goog.global['socket'];

socket['emit'](
    'setUserInfo', 
    goog.global['USER_ID'], 
    goog.global['LANGUAGE_PAIRS'],
    function() {
        var waitingRoutine = ll.WaitingRoutine.getInstance();
        waitingRoutine.start(
            goog.global['socket'],
            function(response) {
                alert(response);
            });
    });

