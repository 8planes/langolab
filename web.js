var express = require('express');

var app = express.createServer(express.logger());
var redis = require('redis-url').createClient(process.env.REDISTOGO_URL);
var mongoose = require('mongoose');

mongoose.connect(process.env.MONGO_URL || "mongodb://localhost/db")

require("./models/testmodel.js");

var TestModel = mongoose.model("TestModel");

app.get('/', function(request, response) {
    redis.incr('nextid', function(err, id) {
        var testModel = new TestModel();
        testModel.number = id;
        testModel.username = "what" + id;
        testModel.save(function(err) {
            // TODO: do something here.
            console.log(err);
        });
        response.send("Hello world " + id);
    });
});

var port = process.env.PORT || 3000;

app.listen(port, function() {
    console.log("Listening on " + port);
});
