var mongoose = require('mongoose');

var MatchSchema = new mongoose.Schema({
    user0: mongoose.Schema.ObjectId,
    user1: mongoose.Schema.ObjectId,
    user0LastPing: Date,
    user1LastPing: Date,
    dateStarted: Date
});

var Match = exports = module.exports =
    mongoose.model("match", MatchSchema);

MatchSchema.statics.start = function(user0id, user1id, callback) {
    var toObjectID = function(id) {
        return typeof id == "string" ? 
            new mongoose.Types.ObjectId(id) : id;
    };
    var match = new Match();
    match.user0 = toObjectID(user0id);
    match.user1 = toObjectID(user1id);
    match.dateStarted = new Date();
    match.save(function(err) {
        callback(err ? null : match);
    });
};

