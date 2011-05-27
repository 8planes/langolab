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

goog.provide('ll.TimeChart');

goog.require('ll');
goog.require('goog.ui.Component');
goog.require('goog.dom.classes');

/**
 * @constructor
 */
ll.TimeChart = function() {
    goog.ui.Component.call(this);
};
goog.inherits(ll.TimeChart, goog.ui.Component);

ll.TimeChart.prototype.enterDocument = function() {
    ll.TimeChart.superClass_.enterDocument.call(this);
    var elem = this.getElement();
    goog.dom.classes.add(elem, 'timechart');
    ll.loadCode(
        ll.config('dygraphJS'),
        function() {
            return goog.isDefAndNotNull(window['Dygraph']);
        },
        goog.bind(this.chartsLoaded_, this));
    goog.dom.setTextContent(elem, "Loading...");
};

ll.TimeChart.prototype.chartsLoaded_ = function() {
    ll.rpc('fetch_chart', {},
           goog.bind(this.dataLoaded_, this));
};

ll.TimeChart.prototype.dataLoaded_ = function(data) {
    var elem = this.getElement();
    goog.dom.removeChildren(elem);
    new window["Dygraph"](
        elem, 
        function() { return data['text']; },
        { "title": "Speakers you match with over the last 5 days",
          "ylabel": "Number of speakers",
          "legend": "always", 
          "labelsDivStyles": { 'fontSize': '12px', 'textAlign': 'right' }});
};