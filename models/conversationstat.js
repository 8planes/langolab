var mongoose = require('mongoose'),
    utils = require('../utils'),
    languages = require('../languages'),
    settings = require('../settings');

var fullLanguageName = function(l) {
    return languages.languageMap[l];
};

var ConversationStatSchema = new mongoose.Schema({
    nativeLanguage: { 
        type: String, 
        required: true, 
        get: fullLanguageName },
    foreignLanguage: { 
        type: String, 
        required: true,
        get: fullLanguageName },
    weekStartDate: { type: Date, required: true, index: true},
    count: { type: Number }
});

mongoose.model('conversationStat', ConversationStatSchema);

ConversationStatSchema.index(
    { nativeLanguage: 1, foreignLanguage: 1, week_start_date: 1 },
    { unique: true });

ConversationStatSchema.index({ count: -1 });

ConversationStatSchema.statics.increment = 
    function(nativeLanguage, foreignLanguage, date) {
        var curDate = utils.utcDate(date);
        curDate.setDate(curDate.getDate() - 6);
        while (curDate <= date) {
            this.update({ nativeLanguage: nativeLanguage,
                          foreignLanguage: foreignLanguage,
                          date: utils.ut },
                        { $inc: { count: 1 } },
                        { upsert: true });
            curDate.setDate(curDate.getDate() + 1);
        }
    };

ConversationStatSchema.statics.topForLastWeek = function(num, callback) {
    var startDate = utils.utcDate(new Date());
    startDate.setDate(startDate.getDate() - 6);
    this.where('weekStartDate', startDate)
        .desc('count')
        .limit(num)
        .run(function(err, docs) {
            callback(docs);
        });
};

var ConversationStat = exports = module.exports = 
    mongoose.model("conversationstat", ConversationStatSchema);