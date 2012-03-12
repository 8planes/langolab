var mongoose = require('mongoose'),
_und = require('underscore');

var LanguagePairSchema = new mongoose.Schema({
    foreignLanguage: String,
    nativeLanguage: String
});

var WaitingUserSchema = new mongoose.Schema({
    userID: { type: mongoose.Schema.ObjectId, unique: true },
    lastPing: Date,
    languages: [LanguagePairSchema]
});

WaitingUserSchema.index(
    { lastPing: -1, 
      'languages.foreignLanguage': 1,
      'languages.nativeLanguage': 1});

WaitingUser.statics.ping = 
    function(userID, languagePairs, callback) 
{
    if (typeof userID == "string") {
        userID = new mongoose.Schema.ObjectId(userID);
    }
    languagePairs = _und.map(
        languagePairs,
        function(pair) {
            return {
                foreignLanguage: pair[1],
                nativeLanguage: pair[0]
            };
        });    
    console.log(langaugePairs);
    this.update(
        { userID: userID },
        { lastPing: new Date(),
          langauges: languagePairs },
        { upsert: true},
        function(err, numAffected) {
            callback();
        });
};

var WaitingUser = exports = module.exports = 
    mongoose.model("waitinguser", WaitingUserSchema);
