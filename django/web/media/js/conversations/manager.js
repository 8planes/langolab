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

goog.provide('ll.Manager');

goog.require('ll.Swf');
goog.require('goog.events.EventHandler');
goog.require('ll.WaitingManager');

/**
 * @constructor
 */
ll.Manager = function() {
    this.handler_ = new goog.events.EventHandler(this);
    this.statusElem_ = goog.dom.getElement('status');
    this.nearID_ = null;
};
goog.addSingletonGetter(ll.Manager);

ll.Manager.prototype.logger_ = goog.debug.Logger.getLogger('ll.Manager');

ll.Manager.prototype.init = function() {
    var swf = ll.Swf.getInstance();
    this.handler_.
        listen(
            swf,
            ll.Swf.Event.READY,
            this.swfReady_).
        listen(
            swf,
            ll.Swf.Event.STATECHANGE,
            this.swfStateChange_);
    swf.init();
};

ll.Manager.prototype.swfReady_ = function(e) {
    this.logger_.info('swfReady with nearID ' + e.nearID);
    this.nearID_ = e.nearID;
    ll.WaitingManager.getInstance().setNearID(e.nearID);
    ll.WaitingManager.getInstance().start();
};
ll.Manager.prototype.showStatus_ = function(status) {
    goog.dom.setTextContent(this.statusElem_, status);
};
ll.Manager.prototype.swfStateChange_ = function(e) {
    if (e.state == 0)
        this.showStatus_('Getting through security settings');
    else if (e.state == 1)
        this.showStatus_('Connecting to server');
    this.logger_.info('swfStateChange with state ' + e.state);
};

if (goog.DEBUG) {
    var debugWindow = new goog.debug.FancyWindow('main');
    debugWindow.setEnabled(true);
    debugWindow.init();
}

ll.Manager.getInstance().init();