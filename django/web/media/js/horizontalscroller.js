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

goog.provide('ll.HorizontalScroller');

goog.require('ll.style');
goog.require('goog.ui.Component');
goog.require('goog.dom.classes');
goog.require('goog.style');
goog.require('goog.Timer');

/**
 * @constructor
 * @extends goog.ui.Component
 * @param {goog.ui.Component} child
 */
ll.HorizontalScroller = function(child) {
    goog.ui.Component.call(this);
    this.child_ = child;
    this.animationTimer_ = new goog.Timer(40);
    /**
     * True when animating left, false when animating right, 
     * null when not animating.
     * @type {?boolean}
     */
    this.animatingLeft_ = null;
    /**
     * current position of animated content
     */
    this.left_ = 0;
};
goog.inherits(ll.HorizontalScroller, goog.ui.Component);

ll.HorizontalScroller.STEP_ = 10;
ll.HorizontalScroller.LEFT_CLASS_NAME = 'leftscroller';
ll.HorizontalScroller.RIGHT_CLASS_NAME = 'rightscroller';

/**
 * @override
 */
ll.HorizontalScroller.prototype.getContentElement = function() {
    return this.container_;
};

ll.HorizontalScroller.prototype.createDom = function() {
    ll.HorizontalScroller.superClass_.createDom.call(this);
    goog.dom.classes.add(this.getElement(), 'll-horizontalscroller');
    var $d = goog.bind(this.getDomHelper().createDom, this.getDomHelper());
    goog.dom.append(
        this.getElement(),
        this.leftScroller_ = 
            $d('div', ll.HorizontalScroller.LEFT_CLASS_NAME),
        this.container_ = $d('div', 'scrollercontainer'),
        this.rightScroller_ = 
            $d('div', ll.HorizontalScroller.RIGHT_CLASS_NAME));
    this.addChild(this.child_, true);
};

ll.HorizontalScroller.prototype.enterDocument = function() {
    ll.HorizontalScroller.superClass_.enterDocument.call(this);
    var contentWidth = goog.style.getSize(this.child_.getElement()).width;
    var containerWidth = goog.style.getSize(this.container_).width;
    this.minimumLeft_ = -contentWidth + containerWidth;
    this.updateScroller_();
    this.getHandler().
        listen(
            this.leftScroller_,
            goog.events.EventType.MOUSEOVER,
            this.scrollerMouseover_).
        listen(
            this.rightScroller_,
            goog.events.EventType.MOUSEOVER,
            this.scrollerMouseover_).
        listen(
            this.leftScroller_,
            goog.events.EventType.MOUSEOUT,
            this.scrollerMouseout_).
        listen(
            this.rightScroller_,
            goog.events.EventType.MOUSEOUT,
            this.scrollerMouseout_).
        listen(
            this.animationTimer_,
            goog.Timer.TICK,
            this.animationTimerTick_);
};

ll.HorizontalScroller.prototype.scrollerMouseoverClass_ = function(left) {
    return (left ? 
            ll.HorizontalScroller.LEFT_CLASS_NAME : 
            ll.HorizontalScroller.RIGHT_CLASS_NAME) + '-over';
};

ll.HorizontalScroller.prototype.scrollerMouseover_ = function(e) {
    var left = e.target == this.leftScroller_;
    goog.dom.classes.add(e.target, this.scrollerMouseoverClass_(left));
    this.animatingLeft_ = !left;
    this.animationTimer_.start();
};

ll.HorizontalScroller.prototype.scrollerMouseout_ = function(e) {
    var left = e.target == this.leftScroller_;
    goog.dom.classes.remove(e.target, this.scrollerMouseoverClass_(left));
    this.animatingLeft_ = null;
    this.animationTimer_.stop();
};

ll.HorizontalScroller.prototype.animationTimerTick_ = function(e) {
    if (this.animatingLeft_) {
        this.left_ = Math.max(
            this.minimumLeft_, this.left_ - ll.HorizontalScroller.STEP_);
    }
    else {
        this.left_ = Math.min(0, this.left_ + ll.HorizontalScroller.STEP_);
    }
    this.updateScroller_();
};

ll.HorizontalScroller.prototype.updateScroller_ = function() {
    goog.style.setStyle(this.child_.getElement(), 'marginLeft', this.left_ + 'px');
    ll.style.setVisible(this.leftScroller_, this.left_ < 0);
    ll.style.setVisible(this.rightScroller_, this.left_ > this.minimumLeft_);
};

/**
 * @override
 */
ll.HorizontalScroller.prototype.disposeInternal = function() {
    ll.HorizontalScroller.superClass_.disposeInternal.call(this);
    this.animationTimer_.dispose();
};