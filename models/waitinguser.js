var mongoose = require('mongoose'),
_und = require('underscore');

var LanguagePairSchema = new mongoose.Schema({
    foreignLanguage: String,
    nativeLanguage: String
});

/**
 * Uses userID as _id.
 */
var WaitingUserSchema = new mongoose.Schema({
    waitStart: { type: Date, index: true },
    languages: [LanguagePairSchema]
});

WaitingUserSchema.index(
    { 'languages.foreignLanguage': 1,
      'languages.nativeLanguage': 1});

/**
 * @param {Array.<Array>} languagePairs Array of pairs.
 * @param {function(?WaitingUser)} callback
 */
function nextAvailableUser(languagePairs, callback) {
    if (languagePairs.length == 0) {
        callback(null);
    }
    else {
        var pingTimeout = new Date(
            new Date().getTime() - PING_THRESHOLD * 1000);
        var languagePair = languagePairs.pop();
        this.findOneAndRemove(
            {
                languages: { 
                    '$elemMatch': {
                        foreignLanguage: languagePair[1],
                        nativeLanguage: languagePair[0]
                    }
                }
            },
            { sort: { waitStart: -1 } },
            function(doc) {
                if (doc) {
                    callback(doc);
                }
                else {
                    nextAvailableUser(languagePairs, callback);
                }
            });
    }
}

WaitingUserSchema.statics.nextAvailableUser = nextAvailableUser;

/**
 * Stops waiting
 */
WaitingUserSchema.statics.stop = function(userID) {
    this.remove({ _id: mongoose.Types.ObjectId(userID) });
};

/**
 * Starts waiting
 */
WaitingUserSchema.statics.start = 
    function(userID, languagePairs, callback) 
{
    var modelLanguagePairs = _und.map(
        languagePairs,
        function(pair) {
            return {
                foreignLanguage: pair[1],
                nativeLanguage: pair[0]
            };
        });
    this.update(
        { _id: userID },
        { waitStart: new Date(),
          languagePairs: modelLanguagePairs },
        { upsert: true },
        function(err, numAffected) {
            callback();
        });
}

var WaitingUser = exports = module.exports = 
    mongoose.model("waitinguser", WaitingUserSchema);
