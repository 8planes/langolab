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

goog.provide('ll.SchedulingWidget');

goog.require('ll.TimeRibbon');
goog.require('ll.HorizontalScroller');

/**
 * @constructor
 * @param {goog.date.Date} startDate
 * @param {Array.<ll.TimeRibbon.PartnerAvailability>=} opt_partnerHours Array of partner availabilities
 * @param {Array.<goog.math.Range>=} opt_myHours My availabilities.
 */
ll.SchedulingWidget = function(startDate, opt_partnerHours, opt_myHours) {
    goog.ui.Component.call(this);
    this.startDate_ = startDate;
    this.partnerHours_ = opt_partnerHours;
    this.myHours_ = opt_myHours;
};
goog.inherits(ll.SchedulingWidget, goog.ui.Component);

ll.SchedulingWidget.prototype.getContentElement = function() {
    return this.contentElement_;
};

ll.SchedulingWidget.prototype.makePartnerHoursDiv_ = function() {
    var partnerHoursDiv = this.c_(
        'div', 'partneravail', 
        this.c_('p', null, 'Times potential language partners are available (so far):'));
    for (var i = ll.TimeRibbon.PartnerAvailability.LOW;
         i <= ll.TimeRibbon.PartnerAvailability.HIGH;
         i++) {
        var text = "";
        if (i == ll.TimeRibbon.PartnerAvailability.LOW) {
            text = "Low";
        }
        else if (i == ll.TimeRibbon.PartnerAvailability.MEDIUM) {
            text = "Medium";
        }
        else {
            text = "High";
        }
        goog.dom.append(
            partnerHoursDiv, 
            this.c_(
                'div', 'partneravailsubdiv',
                this.c_('div', 'availbox availbox-' + i),
                this.c_('div', 'availtext', text + " availability")));
    }
    return partnerHoursDiv;
};

ll.SchedulingWidget.prototype.createDom = function() {
    ll.SchedulingWidget.superClass_.createDom.call(this);
    goog.dom.classes.add(this.getElement(), 'll-schedulingwidget');
    this.c_ = goog.bind(this.getDomHelper().createDom, this.getDomHelper());
    this.contentElement_ = this.c_('div');
    var scheduleContainer = this.c_('div', 'myschedule');
    goog.dom.append(
        scheduleContainer, this.c_('p', null, "Times I'm availabile:"));
    this.myAvailabilityDiv_ = this.c_('div', 'myavail');
    goog.dom.append(scheduleContainer, this.myAvailabilityDiv_);
    goog.dom.append(
        this.getElement(), this.contentElement_, 
        scheduleContainer);

    if (this.partnerHours_) {
        var partnerHoursDiv = this.makePartnerHoursDiv_();
        goog.dom.append(this.getElement(), partnerHoursDiv);
    }

    this.timeRibbon_ = new ll.TimeRibbon(
        this.startDate_, this.partnerHours_, this.myHours_);
    this.scroller_ = new ll.HorizontalScroller(this.timeRibbon_);
    this.addChild(this.scroller_, true);

    this.rangesChanged_();
};

ll.SchedulingWidget.prototype.enterDocument = function() {
    ll.SchedulingWidget.superClass_.enterDocument.call(this);
    this.getHandler().
        listen(
            this.timeRibbon_,
            ll.TimeRibbon.RANGES_CHANGED,
            this.rangesChanged_);
};

ll.SchedulingWidget.prototype.rangesChanged_ = function() {
    var ranges = this.timeRibbon_.getSelectedRanges();
    goog.dom.removeChildren(this.myAvailabilityDiv_);
    for (var i = 0; i < ranges.length; i++) {
        var div = this.c_(
            'div', 'myavailsubdiv',
            this.c_('div', 'availbox my-availbox'),
            this.c_('div', 'availtext', this.timeRibbon_.textForRange(ranges[i].range)));
        if (ranges[i].editing) {
            goog.dom.classes.add(div, 'myavailsubdiv-editing');
        }
        goog.dom.append(this.myAvailabilityDiv_, div);
    }
};