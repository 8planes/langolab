var mongoose = require('mongoose');

var LanguagePairSchema = new mongoose.Schema({
    foreignLanguage: String,
    nativeLanguage: String
});

var WaitingUserSchema = new mongoose.Schema({
    userID: mongoose.Schema.ObjectId,
    waitingSince: Date,
    lastPing: Date,
    languages: [LanguagePairSchema]
});

WaitingUserSchema.index(
    { waitingSince: 1, 
      lastPing: -1, 
      'languages.foreignLanguage': 1,
      'languages.nativeLanguage': 1});

var WaitingUser = exports = module.exports = 
    mongoose.model("waitinguser", WaitingUserSchema);
