TB.setLogLevel(TB.DEBUG);

var session = TB.initSession(OT_SESSIONID);
session.addEventListener(
    "sessionConnected", sessionConnectedHandler);
session.connect(OT_API_KEY, OT_TOKEN);

var publisher;

function sessionConnectedHandler(event) {
    publisher = session.publish("myPublisher");
}
