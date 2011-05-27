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

goog.provide('ll.StompClient');

goog.require('ll.Swf');
goog.require('goog.events.EventTarget');
goog.require('goog.events.EventHandler');

/**
 * @constructor
 */
ll.StompClient = function() {
    goog.events.EventTarget.call(this);
    this.handler_ = new goog.events.EventHandler(this);
    this.handler_.listen(
        ll.Swf.getInstance(),
        [ll.Swf.Event.MESSAGE, ll.Swf.Event.MATCHMESSAGE],
        this.swfMessageHandler_);
    this.logger_ = goog.debug.Logger.getLogger('ll.StompClient');
};
goog.inherits(ll.StompClient, goog.events.EventTarget);
goog.addSingletonGetter(ll.StompClient);

ll.StompClient.Event = {
    MESSAGE: 'message',
    MATCHMESSAGE: 'matchmessage'
};

ll.StompClient.prototype.swfMessageHandler_ = function(e) {
    var eventType = e.type == ll.Swf.Event.MESSAGE ? 
        ll.StompClient.Event.MESSAGE : ll.StompClient.Event.MATCHMESSAGE;
    this.dispatchEvent({
        type: eventType,
        message: e.message
    });
};

ll.StompClient.prototype.disposeInternal = function() {
    ll.StompClient.superClass_.disposeInternal.call(this);
    this.handler_.dispose();
};