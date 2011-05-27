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

goog.provide('ll.WaitingManager');

goog.require('ll');
goog.require('ll.StompClient');

/**
 * @constructor
 */
ll.WaitingManager = function() {
    this.handler_ = new goog.events.EventHandler(this);
    this.nearID_ = null;
    this.logger_ = goog.debug.Logger.getLogger('ll.WaitingManager');
    this.waiting_ = false;
};
goog.addSingletonGetter(ll.WaitingManager);

ll.WaitingManager.prototype.setNearID = function(nearID) {
    this.nearID_ = nearID;
};

ll.WaitingManager.prototype.start = function() {
    this.waiting_ = true;
    this.showFindingMatch_();
    ll.rpc('ping_waiting', 
           { 'near_id': this.nearID_ },
           goog.bind(this.initialPingCompleted_, this));
};

ll.WaitingManager.prototype.initialPingCompleted_ = function(response) {
    ll.rpc('find_match', { 'near_id': this.nearID_ },
           goog.bind(this.initialFindCompleted_, this));
};

ll.WaitingManager.prototype.initialFindCompleted_ = function(response) {
    if (response['status'] == 'matched') {
        this.switchToConversation_(response['near_id']);
    } else {
        this.startWaiting_();
    }
};

ll.WaitingManager.prototype.startWaiting_ = function() {
    this.handler_.listen(
        ll.StompClient.getInstance(),
        ll.StompClient.Event.MESSAGE,
        this.stompMessageReceived_);
    this.showWaitingRoom_();
    this.timer_ = new goog.Timer(10 * 1000);
    this.handler_.listen(
        this.timer_,
        goog.Timer.TICK,
        this.waitingTimerTick_);
    this.timer_.start();
    var chartElem = goog.dom.getElement('chart');
    this.showWaitSpecificElements_(true);
    if (!this.timeChart_) {
        this.timeChart_ = new ll.TimeChart();
        this.timeChart_.decorate(chartElem);
    }
    goog.style.showElement(goog.dom.getElement('share'), true);
};

ll.WaitingManager.prototype.stompMessageReceived_ = function(e) {
    if (e.message['message_type'] == 'matched') {
        this.timer_.stop();
        this.waitingTimerTick_();
    }
};

ll.WaitingManager.prototype.showWaitSpecificElements_ = function(show) {
    goog.array.forEach(
        ['chart', 'waitingExplanation'],
        function(id) {
            goog.style.showElement(goog.dom.getElement(id), show);
        });
};

ll.WaitingManager.prototype.waitingTimerTick_ = function() {
    ll.rpc('ping_waiting', 
           {}, goog.bind(this.waitingPingCompleted_, this));
};

ll.WaitingManager.prototype.waitingPingCompleted_ = function(response) {
    if (response['status'] == 'matched')
        this.switchToConversation_(response['near_id']);
};

ll.WaitingManager.prototype.switchToConversation_ = function(nearID) {
    if (!this.waiting_)
        return;
    this.showWaitSpecificElements_(false);
    this.waiting_ = false;
    this.handler_.removeAll();
    if (this.timer_) {
        this.timer_.stop();
        this.timer_ = null;
    }
    goog.style.showElement(goog.dom.getElement('chart'), false);
    this.showStatus_('You are matched.');
    ll.ConversationManager.getInstance().start(nearID);
};

ll.WaitingManager.prototype.showStatus_ = function(status) {
    goog.dom.setTextContent(
        goog.dom.getElement('status'), status);
};

ll.WaitingManager.prototype.showFindingMatch_ = function() {
    this.showStatus_('Finding a match who speaks ' + ll.languageString());
};

ll.WaitingManager.prototype.showWaitingRoom_ = function() {
    this.showStatus_('Waiting for a match who speaks ' + ll.languageString());
};