

		var map = L.map('map').setView([lat, lon], 14);
		L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg', {
			attribution : 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
			subdomains : 'abcd',
			minZoom : 3,
			maxZoom : 16
		}).addTo(map);

		// L.geoJson(stationsJson).addTo(map);
		// var myLayer = L.geoJson().addTo(map);
		// myLayer.addData(stationsJson);

		//Create SVG element
       	//Width and height
		// a global
	    var w = 400;
	    var h = 200;
	    var hlabels = h + 20;
	    var htimestamp = hlabels + 20;
	    var barPadding = 3;
	    var barWidth = 10;
	    var svg;

/* Visualizing parameters in a station */
		
		d3.json(paramjson, function(error, json) {
			if (error) return console.warn(error);
			console.log([json.records]);		

		// this part scale the transparency of the wings
			var minValue = d3.min(json.records, function(d) {
				return d.value;
			});
			var maxValue = d3.max(json.records, function(d) {
				return d.value;
			});
			var valueScale = d3.scale.linear().domain([minValue, maxValue]).range([0, 1]);
			var rec = ([json.records][0]);
			//var scaled_value = valueScale(rec.value);
			console.log(rec);
	        //Create SVG element
	        var svg = d3.select("#timeseries")
	                                .append("svg")
	                                .attr("width", w)
	                                .attr("height", h);
	
	        svg.selectAll("rect")
	        .data(json.records)
	        .enter()
	        .append("rect")
	         //.attr("x", function(d, i) {
	         //                return i * (w / datasetValues.length);
	         //})
	        .attr("x", function(d, i){return i*(barWidth+barPadding)})
	        .attr("y", function(d) {
	                         return (h-(d.value))})
	         //.attr("width", w / datasetValues.length - barPadding)
	        .attr("width", barWidth)
	        .attr("height", function(d) {
	                         return (d.value)})
	        .attr("fill", function(d) {
	                        return "rgb(0, 0, " + (d.value * 10) + ")";	         
	         })
	        .append("svg:title")
   			.text(function(d) { return d.timestamp; });
	    });
