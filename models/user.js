var mongoose = require('mongoose');

var UserSchema = new mongoose.Schema({
    nickname: { type: String, index: { unique: true, sparse: true }},
    nativeLanguages: [String],
    foreignLanguages: [String]
});

mongoose.model("user", UserSchema);

UserSchema.methods.possibleNicknames = function() {
    if (this.fb) {
        return this.fb.name.full.replace(' ', '');
    }
    else if (this.google) {
        return /([^@]+)@/.exec(this.google.email)[1];
    }
    else if (this.twit) {
        return this.twit.name;
    }
    else {
        return this.login;
    }
};

var User = exports = module.exports = mongoose.model("user", UserSchema);
