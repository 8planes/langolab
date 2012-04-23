var mongoose = require('mongoose'),
    bcrypt = require('bcrypt');

var UserSchema = new mongoose.Schema({
    name: { type: String, required: true, index: { unique: true }},
    email: { type: String, required: false, index: { unique: true, sparse: true }},
    hashedPassword: String,
    salt: String,
    fb: { 
        type: {
            id: String,
            username: String,
            displayName: String,
            lastName: String,
            firstName: String,
            middleName: String,
            gender: String,
            profileURL: String,
        },
        required: false
    },
    nativeLanguages: [String],
    foreignLanguages: [String]
});

UserSchema.index({ 'fb.id': 1 }, { unique: true });

UserSchema.methods.setPassword = function(password, callback) {
    var that = this;
    bcrypt.gen_salt(10, function(err, salt) {
        bcrypt.encrypt(password, salt, function(err, hashedPassword) {
            that.hashedPassword = hashedPassword;
            callback();
        });
    });
};

UserSchema.methods.languagePairs = function() {
    if (!this._languagePairs) {
        var languagePairs = [];
        for (var i = 0; i < this.nativeLanguages.length; i++) {
            for (var j = 0; j < this.foreignLanguages.length; j++) {
                languagePairs.push(
                    [this.nativeLanguages[i], this.foreignLanguages[j]]);
            }
        }
        this._languagePairs = languagePairs;
    }
    return this._languagePairs;
};

UserSchema.methods.authenticate = function(password, callback) {
    bcrypt.compare(password, this.hashedPassword, callback);
};

var User = exports = module.exports = mongoose.model("user", UserSchema);
