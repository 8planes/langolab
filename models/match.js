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