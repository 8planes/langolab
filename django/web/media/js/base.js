/*
Langolab -- learn foreign languages by speaking with random native speakers over webcam.
Copyright (C) 2011 Adam Duston

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

goog.provide('ll');

goog.require('goog.json');
goog.require('goog.net.XhrIo');
goog.require('goog.Uri.QueryData');
goog.require('goog.debug.Logger');
goog.require('goog.string.StringBuffer');
goog.require('goog.dom');
goog.require('goog.events');

ll.config = function(configVar) {
    return window['config'][configVar];
};

ll.logger_ = goog.debug.Logger.getLogger('ll');

ll.pushToGAQ_ = function(pushee) {
    window['_gaq']['push'](pushee);
};

ll.track = function(pageName) {
    ll.pushToGAQ_(['_trackPageview', pageName]);
};

ll.trackAndNavigate = function(pageName, url) {
    ll.track(pageName);
    ll.pushToGAQ_(function() { window.location = url; });
};

ll.rpc = function(methodName, args, opt_callback, opt_errorCallback) {
    ll.logger_.info('ll.rpc called');
    var serializedArgs = goog.object.map(
        args, function(value) { return goog.json.serialize(value); });
    if (goog.DEBUG) {
        ll.logger_.info(methodName + ': ' + 
                        goog.json.serialize(serializedArgs));
    }
    var queryData = new goog.Uri.QueryData();
    queryData.extend(serializedArgs);
    goog.net.XhrIo.send(
        ll.config('rpcURL') + methodName,
        function(event) {
            if (!event.target.isSuccess()) {
                if (goog.DEBUG) {
                    ll.logger_.info(methodName + " failed");
                }
                if (opt_errorCallback)
                    opt_errorCallback();
            }
            else {
                if (goog.DEBUG) {
                    ll.logger_.info(methodName + " returned: " +
                                    event.target.getResponseText());
                }
                if (opt_callback)
                    opt_callback(event.target.getResponseJson());
            }
        },
        "POST",
        queryData.toString(),
        null, 15000);
};

ll.languageString = function() {
    var languages = ll.config('languages');
    var string = new goog.string.StringBuffer();
    for (var i = 0; i < languages.length; i++) {
        string.append(languages[i][1]);
        if (i < languages.length - 2)
            string.append(', ');
        else if (i < languages.length - 1)
            string.append(' or ');
    }
    return string.toString();
};

ll.loadCode = function(url, test, callback) {
    if (test()) {
        callback();
        return;
    }
    var s = goog.dom.createDom(
        'script',
        { 'type': 'text/javascript',
          'async': 'true',
          'src': url });
    var first = goog.dom.getElementsByTagNameAndClass('script')[0];
    goog.dom.insertSiblingBefore(s, first);
    var timer = new goog.Timer(100);
    goog.events.listen(
        timer,
        goog.Timer.TICK,
        function(e) {
            if (test()) {
                timer.stop();
                callback();
            }
        });
    timer.start();
};
