var express = require('express'),
messages = require('express-messages'),
MongoStore = require('connect-mongo'),
settings = require('./settings.js'),
mongoose = require('mongoose');

mongoose.connect(settings.MONGO_DB_URL);

var app = express.createServer();

app.set("views", __dirname + "/views");
app.set("view engine", "jade");
app.set("view options", { layout: false });

app.dynamicHelpers({
    messages: messages,
    base: function(){
        // return the app's mount-point                                                                               
        // so that urls can adjust. For example                                                                       
        // if you run this example /post/add works                                                                    
        // however if you run the mounting example                                                                    
        // it adjusts to /blog/post/add                                                                               
        return '/' == app.route ? '' : app.route;
    }
});

app.configure(function() {
    app.use(express.logger('\x1b[33m:method\x1b[0m \x1b[32m:url\x1b[0m :response-time'));
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(express.cookieParser(settings.COOKIE_SECRET));
    app.use(express.session({
        secret: settings.SESSION_SECRET,
        store: new MongoStore({ db: settings.MONGO_DB })
    }));
    app.use(app.router);
    app.use(express.static(__dirname + '/public'));
    app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

require('./routes/site')(app);

var port = process.env.PORT || 3000;

app.listen(port, function() {
    console.log("Listening on " + port);
});
