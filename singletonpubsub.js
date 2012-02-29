var settings = require('./settings.js');
var redis = require('redis-url').createClient(settings.REDIS_URL);

var listeners = {};

function publish(channel, message) {
    var packet = JSON.stringify({
        channel: channel,
        message: message
    });
    redis.publish(channel, packet);
}

function subscribe(channel, listener) {
    if (!listener) {
        unsubscribe(channel);
    }
    else {
        listeners[channel] = listener;
    }
}

function unsubscribe(channel) {
    delete listeners[channel];
}

redis.on("message", function(channel, message) {
    var packet = JSON.parse(message);
    var listener = listeners[packet.channel];
    if (listener) {
        listener(packet.message);
    }
});

redis.subscribe("allmessages");

exports.publish = publish;
exports.subscribe = subscribe;
exports.unsubscribe = unsubscribe;
