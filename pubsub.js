var settings = require('./settings.js');
var redis = require('redis-url').createClient(settings.REDIS_URL);
var _und = require('underscore');

var channels = {};
var userIDs = {};
var REDIS_CHANNEL = "allmessages";

function publish(channel, opt_userID, message) {
    var packet = JSON.stringify({
        'channel': channel,
        'userID': opt_userID,
        'message': message
    });
    redis.publish(REDIS_CHANNEL, packet);
}

function subscribe(channel, userID, listener) {
    userID = userID.toString();
    if (!listener) {
        unsubscribe(channel, userID);
    }
    else {
        if (!channels[channel]) {
            channels[channel] = {};
        }
        channels[channel][userID] = listener;
        if (!userIDs[userID]) {
            userIDs[userID] = {};
        }
        userIDs[userID][channel] = "a";
    }
}

function unsubscribe(channel, userID) {
    userID = userID.toString();
    if (channels[channel]) {
        delete channels[channel][userID];
    }
    if (userIDs[userID]) {
        delete userIDs[userID][channel];
    }
}

function unsubscribeAll(userID) {
    userID = userID.toString();
    var usersChannels = userIDs[userID];
    if (!usersChannels) {
        return;
    }
    for (channel in usersChannels) {
        delete channels[channel][userID];
    }
    delete userIDs[userID];
}

redis.on("message", function(channel, message) {
    var packet = JSON.parse(message);
    var channel = packet['channel'];
    var userID = packet['userID'];
    var message = packet['message'];
    var userIDs = channels[channel];
    if (!userIDs) {
        return;
    }
    var functions = [];
    if (userID && userIDs[userID]) {
        functions.push(userIDs[userID]);
    }
    else if (!userID) {
        for (var userID in userIDs) {
            functions.push(userIDs[userID]);
        }
    }
    _und.each(functions, function(fn) { fn(message); });
});

redis.subscribe(REDIS_CHANNEL);

exports.publish = publish;
exports.subscribe = subscribe;
exports.unsubscribe = unsubscribe;
exports.unsubscribeAll = unsubscribeAll;
