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


ll.SchedulingWidget = function() {
    goog.ui.Component.call(this);
    
};
goog.inherits(ll.SchedulingWidget, goog.ui.Component);

ll.SchedulingWidget.prototype.getContentElement = function() {
    return this.contentElement_;
};

ll.SchedulingWidget.prototype.createDom = function() {
    ll.SchedulingWidget.superClass_.createDom.call(this);
    goog.dom.classes.add(this.getElement(), 'll-schedulingwidget');
    this.c_ = goog.bind(this.getDomHelper().createDom, this.getDomHelper());
    this.contentElement_ = this.c_('div');
    var scheduleContainer = this.c_('div');
    goog.dom.append(
        scheduleContainer, this.c_('p', null, "Times I'm availabile:"));
    this.scheduleTextDiv_ = this.c_('div');
    goog.dom.append(scheduleContainer, this.scheduleTextDiv_);
    goog.dom.append(
        this.getElement(), this.contentElement_, 
        scheduleContainer);
    this.timeRibbon_ = new ll.TimeRibbon();
    this.addChild(this.timeRibbon_, true);
};

ll.SchedulingWidget.prototype.enterDocument = function() {
    ll.SchedulingWidget.superClass_.enterDocument.call(this);
    this.getHandler().
        listen(
            this.timeRibbon_,
            ll.TimeRibbon.RANGES_CHANGED,
            this.rangesChanged_);
};

ll.SchedulingWidget.prototype.rangesChanged_ = function(e) {
    var ranges = this.timeRibbon_.getSelectedRanges();
    goog.dom.removeChildren(this.scheduleTextDiv_);
    var ul = this.c_('ul', 'll-schedule');
    for (var i = 0; i < ranges.length; i++) {
        goog.dom.append(ul, this.c_(
            'li', 
            (ranges[i].editing ? 'editing' : null), 
            this.timeRibbon_.textForRange(ranges[i].range)));
    }
    goog.dom.append(this.scheduleTextDiv_, ul);
};