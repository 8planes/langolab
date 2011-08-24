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

goog.provide('ll.TimeRibbon');

goog.require('goog.date.DateTime');

ll.TimeRibbon = function() {
    goog.ui.Component.call(this);
    this.currentDateTime_ = new goog.date.DateTime();
    this.startDateTime_ = new goog.date.DateTime(
        this.currentDateTime_.getYear(), 
        this.currentDateTime_.getMonth(),
        this.currentDateTime_.getDate());
    this.startIndex_ = this.currentDateTime_.getHours();
    if (goog.DEBUG) {
        this.logger_ = goog.debug.Logger.getLogger('ll.TimeRibbon');
    }
};
goog.inherits(ll.TimeRibbon, goog.ui.Component);

ll.TimeRibbon.NUM_DAYS = 4;

ll.TimeRibbon.prototype.createDom = function() {
    ll.TimeRibbon.superClass_.createDom.call(this);
    goog.dom.classes.add(this.getElement(), 'll-timeribbon');
    this.hours_ = [];
    var numHours = ll.TimeRibbon.NUM_DAYS * 24;
    var hourDiv;
    for (var i = 0; i < numHours; i++) {
        hourDiv = this.getDomHelper().createDom('div');
        if (i % 24 == 0) {
            goog.dom.classes.add(hourDiv, 'daydiv');
        }
        if (i == numHours - 1) {
            goog.dom.classes.add(hourDiv, 'endday');
        }
        this.hours_.push(hourDiv);
        goog.dom.append(this.getElement(), hourDiv);
    }
};

ll.TimeRibbon.prototype.enterDocument = function() {
    ll.TimeRibbon.superClass_.enterDocument.call(this);
    for (var i = 0; i < this.hours_.length; i++) {
        this.addHourListener_(i);
    }
};

ll.TimeRibbon.prototype.addHourListener_ = function(index) {
    this.getHandler().
        listen(
            this.hours_[index],
            goog.events.EventType.MOUSEOVER,
            goog.bind(this.hourMouseOver_, this, index)).
        listen(
            this.hours_[index],
            goog.events.EventType.MOUSEOUT,
            goog.bind(this.hourMouseOut_, this, index));
};

ll.TimeRibbon.prototype.hourMouseOver_ = function(index) {
    goog.dom.classes.add(this.hours_[index], 'dayover');
};

ll.TimeRibbon.prototype.hourMouseOut_ = function(index) {
    goog.dom.classes.remove(this.hours_[index], 'dayover')
};

