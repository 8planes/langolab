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

goog.provide('ll.ConversationManager');

goog.require('goog.dom');
goog.require('goog.style');
goog.require('goog.Timer');
goog.require('goog.events.EventHandler');

/**
 * @constructor
 */
ll.ConversationManager = function() {
    this.handler_ = new goog.events.EventHandler(this);
    this.nextLink_ = goog.dom.getElement('nextLink');
    this.timer_ = null;
};
goog.addSingletonGetter(ll.ConversationManager);

ll.ConversationManager.prototype.start = function(matchNearID) {
    this.matchID_ = matchNearID;
    ll.Swf.getInstance().matchWith(matchNearID);
    goog.style.showElement(this.nextLink_, true);
    this.timer_ = new goog.Timer(30 * 1000)
    this.handler_.
        listen(
            this.nextLink_,
            'click',
            this.nextClicked_).
        listen(
            this.timer_,
            goog.Timer.TICK,
            this.pingConversation_);
};

ll.ConversationManager.prototype.pingConversation_ = function(e) {
    ll.rpc('ping_conversation', {})
};

ll.ConversationManager.prototype.nextClicked_ = function(e) {
    e.preventDefault();
    this.handler_.removeAll();
    if (this.timer_) {
        this.timer_.stop();
        this.timer_ = null;
    }
    goog.Timer.callOnce(function() {
        goog.style.showElement(this.nextLink_, false);
        this.handler_.removeAll();
        ll.Swf.getInstance().matchEnded();
        ll.WaitingManager.getInstance().start();
    }, null, this);
};
