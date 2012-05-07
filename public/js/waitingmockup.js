$(function() {
    var data = 
        [ { "language": "English|Spanish",
            "data": [[ 1336896000000, 4 ],
                     [ 1337036400000, 8 ]] },
          { "language": "English|German",
            "data": [[ 1336899600000, 5 ],
                     [ 1337036400000, 3 ],
                     [ 1337054400000, 7 ]]}];

    function dataArray(minDate, maxDate, rawArray) {
        var values = [];
        var HOUR = 3600 * 1000;
        var curIndex = 0;
        for (var date = minDate; date <= maxDate; date += HOUR) {
            if (curIndex < rawArray.length && 
                rawArray[curIndex][0] == date) 
            {
                values.push([date, rawArray[curIndex][1]]);
                curIndex++;
            }
            else {
                values.push([date, curIndex == 0 ? null : 0]);
            }
        }
        return values;
    }

    function seriesFromData() {
        var minDate = Math.min.apply(
            null, _.map(data, function(l) {
                return l['data'][0][0];
            }));
        var maxDate = Math.max.apply(
            null, _.map(data, function(l) {
                return l['data'][l['data'].length - 1][0];
            }));
        var series = [];
        for (var i = 0; i < data.length; i++) {
            series.push({
                "name": data[i]['language'],
                "data": dataArray(minDate, maxDate, data[i]['data']) });
        }
        return series;
    }

    var series = seriesFromData();
    var chart = new Highcharts.Chart({
        "chart": {
            "renderTo": "historicalChart",
            "type": "column"
        },
        "tooltip": {
            "formatter": function() {
                var date = new Date(this.x);
                var dateStr = Highcharts.dateFormat("%b %d, %Y - %l %p", this.x);
                var countStr = "No Speakers :(";
                if (this.y > 0) {
                    countStr = this.y + " Speakers"
                }
                return "<b>" + dateStr + "</b><br/>" + countStr;
            }
        },
        "plotOptions": {
            "column": {
                "stacking": "normal",
                "borderWidth": 0,
                "shadow": false,
                "pointPadding": 0,
                "groupPadding": 0
            }
        },
        "title": {
            "text": null
        },
        "xAxis": {
            "type": "datetime"
        },
        "yAxis": {
            "allowDecimals": false,
            "title": {
                "text": "Number of speakers"
            }
        },
        "series": series
    });

});