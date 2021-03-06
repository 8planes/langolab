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

goog.require('goog.ui.Component');
goog.require('goog.date.DateTime');
goog.require('goog.math.Range');
goog.require('goog.i18n.DateTimeFormat');
goog.require('goog.dom.classes');
goog.require('goog.dom');

/**
 * @constructor
 * @param {goog.date.Date} startDate
 * @param {Array.<ll.TimeRibbon.PartnerAvailability>=} opt_partnerHours Array of partner availabilities
 * @param {Array.<goog.math.Range>=} opt_myHours My availabilities.
 */
ll.TimeRibbon = function(startDate, opt_partnerHours, opt_myHours) {
    goog.ui.Component.call(this);
    this.startDateTime_ = new goog.date.DateTime(
        startDate.getYear(), 
        startDate.getMonth(),
        startDate.getDate());
    if (goog.DEBUG) {
        this.logger_ = goog.debug.Logger.getLogger('ll.TimeRibbon');
    }
    this.mouseDown_ = false;
    /**
     * @type {?goog.math.Range}
     */
    this.mouseDownRange_ = null;
    /**
     * @type {?ll.TimeRibbon.PartnerAvailability>=}
     */
    this.partnerHours_ = opt_partnerHours;
    /**
     * Kept in sorted order.
     * @type {Array.<goog.math.Range>}
     */
    this.selectedRanges_ = opt_myHours || [];
    this.dateTimeFormat_ = new goog.i18n.DateTimeFormat("MMM d, h a");
    this.hourFormat_ = new goog.i18n.DateTimeFormat("h a");
    this.mouseOverIndex_ = null;
};
goog.inherits(ll.TimeRibbon, goog.ui.Component);

/**
 * @enum
 */
ll.TimeRibbon.PartnerAvailability = {
    NONE: 0,
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3
};

ll.TimeRibbon.NUM_DAYS = 7;

ll.TimeRibbon.RANGES_CHANGED = 'rangeschanged';

ll.TimeRibbon.rangeComparison_ = function(a, b) {
    return goog.array.defaultCompare(a.start, b.start);
};

ll.TimeRibbon.prototype.createDaysHeader_ = function($d) {
    var daysDiv = $d('div', 'days');
    var dayFormat = new goog.i18n.DateTimeFormat('EEE, MMM d');
    var dateTime = this.startDateTime_.clone();
    for (var i = 0; i < ll.TimeRibbon.NUM_DAYS; i++) {
        goog.dom.append(daysDiv, $d('span', 'day', dayFormat.format(dateTime)));
        dateTime.add(new goog.date.Interval(0, 0, 1));
    }
    return daysDiv;
};

ll.TimeRibbon.prototype.createHoursElements_ = function($d) {
    this.hours_ = [];
    var numHours = ll.TimeRibbon.NUM_DAYS * 24;
    this.hoursDiv_ = $d('div', 'hours');
    var hourSpan, partnerHourSpan, myHourSpan, hasPartnerHour;
    for (var i = 0; i < numHours; i++) {
        hourSpan = this.getDomHelper().createDom('span', 'hour');
        if (i % 24 == 0) {
            goog.dom.classes.add(hourSpan, 'daydiv');
        }
        if (i == numHours - 1) {
            goog.dom.classes.add(hourSpan, 'endday');
        }

        if (this.partnerHours_) {
            partnerHourSpan = $d('span', 'partnerhour');
            goog.dom.classes.add(
                partnerHourSpan, 
                'partnerhour-' + this.partnerHours_[i]);
            goog.dom.append(hourSpan, partnerHourSpan);
        }
        
        myHourSpan = $d('span', 'myhour');
        if (this.partnerHours_) {
            goog.dom.classes.add(myHourSpan, 'myhour-half');
        }
        goog.dom.append(hourSpan, myHourSpan);
        
        this.hours_.push(hourSpan);
        goog.dom.append(this.hoursDiv_, hourSpan);
    }
    this.setSelected_();
};

ll.TimeRibbon.prototype.createDom = function() {
    ll.TimeRibbon.superClass_.createDom.call(this);
    goog.dom.classes.add(this.getElement(), 'll-timeribbon');
    var $d = goog.bind(this.getDomHelper().createDom, this.getDomHelper());

    var daysHeader = this.createDaysHeader_($d);

    this.createHoursElements_($d);

    goog.dom.append(this.getElement(), daysHeader, this.hoursDiv_);
};

ll.TimeRibbon.prototype.enterDocument = function() {
    ll.TimeRibbon.superClass_.enterDocument.call(this);
    var handler = this.getHandler();
    for (var i = 0; i < this.hours_.length; i++) {
        this.addHourListener_(handler, i);
    }
    handler.
        listen(
            this.getDomHelper().getDocument(),
            [goog.events.EventType.MOUSEUP],
            this.mouseUp_).
        listen(
            this.hoursDiv_,
            goog.events.EventType.MOUSEOUT,
            goog.bind(this.hoursMouseOut_, this));
};

ll.TimeRibbon.prototype.addHourListener_ = function(handler, index) {
    handler.
        listen(
            this.hours_[index],
            goog.events.EventType.MOUSEOVER,
            goog.bind(this.hourMouseOver_, this, index)).
        listen(
            this.hours_[index],
            goog.events.EventType.MOUSEOUT,
            goog.bind(this.hourMouseOut_, this, index)).
        listen(
            this.hours_[index],
            goog.events.EventType.MOUSEDOWN,
            goog.bind(this.hourMouseDown_, this, index));
};

ll.TimeRibbon.prototype.hoursMouseOut_ = function(e) {
    if (goog.dom.contains(this.hoursDiv_, e.target) &&
        !goog.dom.contains(this.hoursDiv_, e.relatedTarget)) {
        this.mouseOverIndex_ = null;
        this.dispatchEvent(ll.TimeRibbon.RANGES_CHANGED);
    }
};

ll.TimeRibbon.prototype.hourMouseOver_ = function(index, e) {
    if (goog.dom.contains(this.hours_[index], e.target) &&
        e.relatedTarget &&
        !goog.dom.contains(this.hours_[index], e.relatedTarget)) {
        this.hourMouseOverImpl_(index, e);
    }
};

ll.TimeRibbon.prototype.hourMouseOverImpl_ = function(index, e) {
    if (this.mouseDown_) {
        var startIndex, endIndex;
        if (index > this.lastMouseDownIndex_) {
            startIndex = this.lastMouseDownIndex_ + 1;
            endIndex = index;
        }
        else {
            startIndex = index;
            endIndex = this.lastMouseDownIndex_ - 1;
        }

        if (this.mouseDownRange_) {
            if (index <= this.initialMouseDownIndex_) {
                this.mouseDownRange_.start = index;
                if (index == this.initialMouseDownIndex_) {
                    this.mouseDownRange_.end = index;
                }
            }
            else if (index > this.initialMouseDownIndex_) {
                this.mouseDownRange_.end = index;
            }
        }
        else {
            for (var i = startIndex; i <= endIndex; i++) {
                this.removeFromExistingRange_(i);
            }
        }
        this.coalesceSelectedRanges_();
        this.setSelected_();
        this.lastMouseDownIndex_ = index;
    }
    else {
        goog.dom.classes.add(this.hours_[index], 'hourover');
        this.mouseOverIndex_ = index;
    }
    this.dispatchEvent(ll.TimeRibbon.RANGES_CHANGED);
    
};

ll.TimeRibbon.prototype.coalesceSelectedRanges_ = function() {
    var i = 0;
    while (i < this.selectedRanges_.length - 1) {
        if (this.selectedRanges_[i].end + 1 >= this.selectedRanges_[i + 1].start) {
            this.selectedRanges_[i].end = 
                Math.max(this.selectedRanges_[i].end, 
                         this.selectedRanges_[i + 1].end);
            if (this.mouseDownRange_ == this.selectedRanges_[i + 1]) {
                this.mouseDownRange_ = this.selectedRanges_[i];
            }
            goog.array.removeAt(this.selectedRanges_, i + 1);
        }
        else {
            i++;
        }
    }
};

ll.TimeRibbon.prototype.hourMouseOut_ = function(index, e) {
    if (goog.dom.contains(this.hours_[index], e.target) &&
        e.relatedTarget &&
        !goog.dom.contains(this.hours_[index], e.relatedTarget)) {
        goog.dom.classes.remove(this.hours_[index], 'hourover')
    }
};

ll.TimeRibbon.prototype.hourMouseDown_ = function(index, e) {
    this.mouseDown_ = true;
    this.mouseDownRange_ = this.findMouseDownRange_(index);
    this.initialMouseDownIndex_ = index;
    this.coalesceSelectedRanges_();
    this.lastMouseDownIndex_ = index;
    this.setSelected_();
    e.preventDefault();
    this.mouseOverIndex_ = null;
    this.dispatchEvent(ll.TimeRibbon.RANGES_CHANGED);
};

ll.TimeRibbon.prototype.setSelected_ = function() {
    var curRange = 0;
    var inRange = false;
    for (var i = 0; i < this.hours_.length; i++) {
        if (curRange < this.selectedRanges_.length) {
            if (i < this.selectedRanges_[curRange].start) {
                inRange = false;
            }
            else if (goog.math.Range.containsPoint(this.selectedRanges_[curRange], i)) {
                inRange = true;
            }
            else {
                inRange = false;
                curRange++;
            }
        }
        else {
            inRange = false;
        }
        goog.dom.classes.enable(
            this.hours_[i], 'selected', inRange);

    }
};

ll.TimeRibbon.prototype.mouseUp_ = function(e) {
    this.mouseDown_ = false;
    this.mouseDownRange_ = null;
};
ll.TimeRibbon.prototype.findMouseDownRange_ = function(index) {
    var fromExisting = this.removeFromExistingRange_(index);
    if (fromExisting) {
        return null;
    }
    else {
        var newRange = new goog.math.Range(index, index);
        this.selectedRanges_.push(newRange);
        goog.array.sort(
            this.selectedRanges_, ll.TimeRibbon.rangeComparison_);
        return newRange;
    }
};

ll.TimeRibbon.prototype.findRangeForIndex_ = function(index) {
    return goog.array.find(
        this.selectedRanges_, 
        function(r) {
            return goog.math.Range.containsPoint(r, index);
        });
};

ll.TimeRibbon.prototype.removeFromExistingRange_ = function(index) {
    var existingRange = this.findRangeForIndex_(index);
    if (existingRange) {
        if (existingRange.end == existingRange.start) {
            goog.array.remove(this.selectedRanges_, existingRange);
        }
        else if (index > existingRange.start && index < existingRange.end) {
            this.selectedRanges_.push(new goog.math.Range(index + 1, existingRange.end));
            existingRange.end = index - 1;
            goog.array.sort(
                this.selectedRanges_, ll.TimeRibbon.rangeComparison_);
        }
        else if (index == existingRange.start) {
            existingRange.start += 1;
        }
        else if (index == existingRange.end) {
            existingRange.end -= 1;
        }
        return true;
    }
    else {
        return false;
    }
};

ll.TimeRibbon.prototype.getSelectedRanges = function() {
    var selectedRanges = goog.array.map(
        this.selectedRanges_, 
        function(r) {
            return new ll.TimeRibbon.SelectedRange(r, false);
        });
    if (!goog.isNull(this.mouseOverIndex_)) {
        var range = this.findRangeForIndex_(this.mouseOverIndex_);
        if (!range) {
            selectedRanges.push(new ll.TimeRibbon.SelectedRange(
                new goog.math.Range(this.mouseOverIndex_, 
                                    this.mouseOverIndex_), 
                true));
            goog.array.sort(
                selectedRanges, ll.TimeRibbon.SelectedRange.comparison);
        }
        else {
            var selectedRange = goog.array.find(
                selectedRanges,
                function(s) {
                    return s.range.start == range.start;
                });
            selectedRange.editing = true;
        }
    }
    return selectedRanges;
};

ll.TimeRibbon.prototype.dateForIndex_ = function(index) {
    var dateTime = this.startDateTime_.clone();
    dateTime.add(new goog.date.Interval(0, 0, 0, index));
    return dateTime;
};

ll.TimeRibbon.prototype.textForRange = function(range) {
    var startDateTime = this.dateForIndex_(range.start);
    var endDateTime = this.dateForIndex_(range.end + 1);
    var endDateTimeString;
    if (endDateTime.getDate() == startDateTime.getDate()) {
        endDateTimeString = this.hourFormat_.format(endDateTime);
    }
    else {
        endDateTimeString = this.dateTimeFormat_.format(endDateTime);
    }
    return this.dateTimeFormat_.format(startDateTime) + " to " + endDateTimeString;
};

if (goog.DEBUG) {
    // for testing only
    ll.TimeRibbon.prototype.hourElement = function(index) {
        return this.hours_[index];
    };
}

/**
 * @constructor
 * @param {goog.math.Range} range
 * @param {boolean} editing
 */
ll.TimeRibbon.SelectedRange = function(range, editing) {
    this.range = range;
    this.editing = editing;
};

ll.TimeRibbon.SelectedRange.comparison = function(a, b) {
    return ll.TimeRibbon.rangeComparison_(a.range, b.range);
};

if (goog.DEBUG) {
    ll.TimeRibbon.SelectedRange.prototype.toString = function() {
        return this.range.toString() + ", " + this.editing;
    };
}