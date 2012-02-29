exports.inviteChannel = function(userID) {
    return "invite" + userID;
}

exports.invitationResponseChannel = function(token) {
    return "invres" + token;
}

exports.invitationConfirmationChannel = function(token) {
    return "invcon" + token;
}
