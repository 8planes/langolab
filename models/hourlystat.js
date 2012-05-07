var mongoose = require('mongoose'),
    utils = require('../utils'),
    languages = require('../languages'),
    settings = require('../settings');

var fullLanguageName = function(l) {
    return languages.LANGUAGE_MAP[l];
};

var HourlyStatSchema = new mongoose.Schema({
    nativeLanguage: { 
        type: String, 
        required: true, 
        get: fullLanguageName },
    foreignLanguage: { 
        type: String, 
        required: true,
        get: fullLanguageName },
    date: { type: Date, required: true, index: true},
    utcHourStart: { type: Number, required: true },
    count: { type: Number }
});

HourlyStatSchema.index(
    { nativeLanguage: 1, foreignLanguage: 1, date: 1, utcHourStart: 1 },
    { unique: true });

HourlyStatSchema.statics.increment = 
    function(nativeLanguage, foreignLanguage)
{
    var curDate = utils.utcDate(new Date());
    var curHour = new Date().getUTCHours();
    this.update({ nativeLanguage: nativeLanguage,
                  foreignLanguage: foreignLanguage,
                  date: curDate,
                  utcHourStart: curHour },
                { $inc: { count: 1 } },
                { upsert: true },
                function(err, numAffected) {});
};

var HourlyStat = exports = module.exports = 
    mongoose.model("hourlystat", HourlyStatSchema);
