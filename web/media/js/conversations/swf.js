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

goog.provide('ll.Swf');

goog.require('goog.events.EventTarget');
goog.require('goog.json');
goog.require('goog.debug.Logger');
goog.require('goog.asserts');

/**
 * @constructor
 */
ll.Swf = function() {
    goog.events.EventTarget.call(this);
    this.swfID_ = 'swf' + (ll.Swf.idCount_++);
    this.initialized_ = false;
};
goog.inherits(ll.Swf, goog.events.EventTarget);
goog.addSingletonGetter(ll.Swf);

ll.Swf.idCount_ = 0;
ll.Swf.Event = {
    MESSAGE: 'message',
    MATCHMESSAGE: 'matchmessage',
    READY: 'ready',
    STATECHANGE: 'statechange'
};

ll.Swf.prototype.logger_ =
    goog.debug.Logger.getLogger('ll.Swf');

ll.Swf.prototype.init = function() {
    goog.asserts.assert(!this.initialized_);
    this.initialized_ = true;
    this.exportSymbols_();
    var params = { 'allowScriptAccess': 'always', 'wmode': 'transparent' };
    var atts = { 'id': this.swfID_ };
    window['swfobject']['embedSWF'](
        ll.config('swfURL'), 'swf', '480', '440', '10.0.0', null,
        ll.config('flashVars'), params, atts);
};

ll.Swf.prototype.exportSymbols_ = function() {
    var exports = [
        ['stateChange', this.stateChange_],
        ['ready', this.ready_],
        ['messageReceived', this.messageReceived_],
        ['matchMessageReceived', this.matchMessageReceived_],
        ['flashDebug', this.flashDebug_]];
    goog.array.forEach(
        exports, 
        function(e) {
            goog.exportSymbol(
                'swfout.' + e[0],
                goog.bind(e[1], this));
        }, this);
    goog.exportSymbol('swfout.track', ll.track);
};

ll.Swf.prototype.stateChange_ = function(state) {
    this.dispatchEvent({
        type: ll.Swf.Event.STATECHANGE,
        state: state
    });
};

ll.Swf.prototype.ready_ = function(nearID) {
    this.dispatchEvent({
        type: ll.Swf.Event.READY,
        nearID: nearID
    });
};

ll.Swf.prototype.messageReceived_ = function(message) {
    if (goog.DEBUG) {
        this.logger_.info('message received: ' + message);
    }
    this.dispatchEvent({
        type: ll.Swf.Event.MESSAGE,
        message: goog.json.parse(message)
    });
};

ll.Swf.prototype.matchMessageReceived_ = function(message) {
    if (goog.DEBUG) {
        this.logger_.info('match message received: ' + message);
    }
    this.dispatchEvent({
        type: ll.Swf.Event.MATCHMESSAGE,
        message: goog.json.parse(message)
    });
};

ll.Swf.prototype.flashDebug_ = function(message) {
    this.logger_.info('flash debug: ' + message);
};

ll.Swf.prototype.getSwf_ = function() {
    return goog.dom.getElement(this.swfID_);
};

/**
 * @param {string} matchID The nearID of the match.
 */
ll.Swf.prototype.matchWith = function(matchID) {
    this.logger_.info('matching with ' + matchID);
    this.getSwf_()['matchWith'](matchID);
};

ll.Swf.prototype.matchEnded = function() {
    this.getSwf_()['matchEnded']();
};