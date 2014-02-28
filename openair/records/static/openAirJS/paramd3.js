
var map = L.map('map').setView([lat, lon], 14);
L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg', {
	attribution : 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
	subdomains : 'abcd',
	minZoom : 3,
	maxZoom : 18
}).addTo(map);

// stations_data = d3.json(stationsJson)
// L.geoJson(stationsJson).addTo(map);
// var myLayer = L.geoJson().addTo(map);
// myLayer.addData(stationsJson);

// define chart size:
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 500 - margin.left - margin.right,
    chartHeight = 300 - margin.top - margin.bottom;

var barWidth = 10;
var barHeight = chartHeight*0.75;

// define paddings:
var barPadding = 3;
var padding = 30;

// scales:
var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([barHeight, 0]);

var colorScale = d3.scale.linear()
    .range([0, 255]);

// axis:
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

// defining the chart:
var chart = d3.select("#timeseries")
    .attr("width", width + margin.left + margin.right)
    .attr("height", barHeight + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// calling the JSON file:
d3.json(paramjson, function(error, json) {
			if (error) return console.warn(error);
			console.log([json.all_records])
			console.log([json.records])
	// defining data:
	data = json.records.slice(0,24)
	dataAll = json.all_records;
	var maxValue = d3.max(data, function(d) { return d.value; });
	var maxDomain = Math.max(maxValue, total_average_value);
	x.domain(data.map(function(d) { return d.timestamp; }));
	y.domain([0, maxDomain]);
	colorScale.domain([d3.min(data, function(d) { return d.value; }), maxDomain]);

// draw axis:
	chart.append("g")
	  .attr("class", "x axis")
	  .attr("transform", "translate(0," + barHeight + ")")
	  .call(xAxis)
	  .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "0.5em")
            .attr("dy", "-0.5em")
            .attr("transform", "rotate(90)");
	chart.append("g")
	  .attr("class", "y axis")
	  .call(yAxis)
	  .selectAll("text")  
      .style("text-anchor", "end")
      .attr("align", "right")
      .attr("dx", "-1em")
      .attr("dy", "0.3em");

	// draw bars:
	chart.selectAll(".bar")
	  .data(data)
	  .enter().append("rect")
	  .attr("class", "bar")
	  .attr("x", function(d) { return x(d.timestamp); })
	  .attr("y", function(d) { return y(d.value); })
	  .attr("height", function(d) { return barHeight - y(d.value); })
	  .attr("width", x.rangeBand())
	  .attr("fill", function(d) {
	     return "rgb(0, 0, " + Math.round(colorScale(d.value)) + ")";	         
	     })
	// add texts when hover:
	  .append("svg:title")
	  .text(function(d) { return d.value + "\n" + 
	  					d.hour + ":" + d.minutes + 
	  					"\n" + d.day + "/" + d.month + "/" + d.year + 
	  					"\n" + average_value; });

	// draw an average line...
	console.log(json.average_value);
	//average_value = json.average_value;

	var stationAverage = chart.append("svg:line")
	    .attr("x1", 0)
	    .attr("y1", y(average_value))
	    .attr("x2", width)
	    .attr("y2", y(average_value))
	    .style("stroke", "rgb(124,255,0)")
	    .append("svg:title")
	    .text(function(d) { return "ממוצע בתחנה: " + average_value; });


	var totalAverage = chart.append("svg:line")
	    .attr("x1", 0)
	    .attr("y1", y(total_average_value))
	    .attr("x2", width)
	    .attr("y2", y(total_average_value))
	    .style("stroke", "rgb(124,0,255)")
	    .text(function(d) { return "ממוצע כללי: " + total_average_value; });

});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
};
