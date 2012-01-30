var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var TestModel = new Schema({
    number: Number,
    username: String
});

mongoose.model("TestModel", TestModel);