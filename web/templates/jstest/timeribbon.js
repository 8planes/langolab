{% extends "jstest/base.html" %}

{% block requires %}
goog.require('ll.TimeRibbon');
{% endblock %}

{% block testscript %}
var timeribbon;

function setUp() {
    timeribbon = new ll.TimeRibbon();
}

function tearDown() {
    timeribbon.dispose();
}

function assertRanges(ranges) {
    var selectedRanges = timeribbon.getSelectedRanges();
    assertEquals(ranges.length, selectedRanges.length);
    for (var i = 0; i < ranges.length; i++) {
        var range = ranges[i];
        var selectedRange = null;
        for (var j = 0; j < selectedRanges.length && selectedRange == null; j++) {
            if (selectedRanges[j].start == range[0] && 
                selectedRanges[j].end == range[1])
                selectedRange = selectedRanges[j];
        }
        assertNotNull(selectedRange);
    }
    for (var i = 0; i < ll.TimeRibbon.NUM_DAYS * 24; i++) {
        var range = null;
        for (var j = 0; j < ranges.length && range == null; j++) {
            if (ranges[j][0] <= i &&
                ranges[j][1] >= i)
                range = ranges[j];
        }
        var hasSelectedClass = goog.array.contains(
            goog.dom.classes.get(timeribbon.hourElement(i)),
            'selected');
        assertEquals(range != null, hasSelectedClass);
    }
}

function mouseDownAndOut(index) {
    goog.testing.events.fireMouseDownEvent(timeribbon.hourElement(index));
    mouseOut(index);
}

function mouseOverAndOut(index) {
    mouseOver(index);
    mouseOut(index);
}

function mouseOverAndUp(index) {
    mouseOver(index);
    mouseUp(index);
}

function mouseOut(index) {
    goog.testing.events.fireMouseOutEvent(timeribbon.hourElement(index));
}

function mouseOver(index) {
    goog.testing.events.fireMouseOverEvent(timeribbon.hourElement(index));
}

function mouseUp(index) {
    goog.testing.events.fireMouseUpEvent(timeribbon.hourElement(index));
}

function testSelectSectionBasic() {
    timeribbon.render();

    mouseDownAndOut(3);
    mouseOver(4);
    mouseUp(4);    
    mouseOverAndOut(5);
    mouseOver(6);

    assertRanges([[3, 4]]);
}

function testSelectionSkipping() {
    timeribbon.render();

    mouseDownAndOut(3);
    mouseOver(5);

    assertRanges([[3, 5]]);
}

function testContiguousRanges() {
    timeribbon.render();

    mouseDownAndOut(3);
    mouseOverAndUp(4);
    mouseDownAndOut(5);
    mouseOver(6);

    assertRanges([[3, 6]]);
}

function testSelectThenGoBack() {
    timeribbon.render();

    mouseDownAndOut(3);
    mouseOverAndOut(4);
    mouseOverAndOut(5);
    mouseOver(4);

    assertRanges([[3, 4]]);
}

function testUnselectSkipping() {
    timeribbon.render();

    mouseDownAndOut(3);
    mouseOverAndUp(5);
    mouseDownAndOut(5);
    mouseOverAndUp(3);

    assertRanges([]);
}


{% endblock %}
