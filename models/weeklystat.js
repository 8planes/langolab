var mongoose = require('mongoose'),
    utils = require('../utils'),
    languages = require('../languages'),
    settings = require('../settings');

var fullLanguageName = function(l) {
    return languages.LANGUAGE_MAP[l];
};

var WeeklyStatSchema = new mongoose.Schema({
    nativeLanguage: { 
        type: String, 
        required: true, 
        get: fullLanguageName },
    foreignLanguage: { 
        type: String, 
        required: true,
        get: fullLanguageName },
    weekStartDate: { type: Date, required: true },
    count: { type: Number }
});

WeeklyStatSchema.index(
    { nativeLanguage: 1, foreignLanguage: 1, weekStartDate: 1 },
    { unique: true });

WeeklyStatSchema.index({ weekStartDate: 1, count: -1 });

WeeklyStatSchema.statics.increment = 
    function(nativeLanguage, foreignLanguage) {
        var curDate = utils.utcDate(new Date());
        var lastDate = utils.utcDate(new Date());
        curDate.setDate(curDate.getDate() - 6);
        while (curDate <= lastDate) {
            this.update({ nativeLanguage: nativeLanguage,
                          foreignLanguage: foreignLanguage,
                          weekStartDate: new Date(curDate.getTime()) },
                        { $inc: { count: 1 } },
                        { upsert: true },
                        function(err, numAffected) {});
            curDate.setDate(curDate.getDate() + 1);
        }
    };

WeeklyStatSchema.statics.topForLastWeek = function(num, callback) {
    var startDate = utils.utcDate(new Date());
    startDate.setDate(startDate.getDate() - 6);
    this.where('weekStartDate', startDate)
        .desc('count')
        .limit(num)
        .run(function(err, docs) {
            callback(docs);
        });
};

var WeeklyStat = exports = module.exports = 
    mongoose.model("weeklystat", WeeklyStatSchema);
