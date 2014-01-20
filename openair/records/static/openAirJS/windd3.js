var map = L.map('map').setView([lat, lon], 18);
L.tileLayer('http://{s}.tile.cloudmade.com/8897a64b9ba14c60ac9fa07924a23e40/997/256/{z}/{x}/{y}.png', {
	attribution : 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
	maxZoom : 18
}).addTo(map);

// constants
var centerX = 250;
var centerY = centerX;
var SPEED_CIRCLES = [0, 2, 4, 6, 8, 10];
var windRoseRadius = 10;

// d3 scales
var speedColorScale = d3.scale.category20c().domain([0, 50]);
var directionScale = d3.scale.linear().domain([0, 360]).range([0, 2 * Math.PI]);
var speedScale = d3.scale.linear().domain([0, 100]).range([0, 1000]);

// calling json for station's windrose
var data = d3.json(windJson, function(error, json) {
	if (error)
		return console.warn(error);

	// d3 element for windrose (not on the map)
	var vis = d3.select("#windrose");
	var arc = d3.svg.arc().innerRadius(windRoseRadius).outerRadius(function(d) {
		return (speedScale(d.speed) + windRoseRadius);
	}).startAngle(function(d) {
		return directionScale(d.direction + 10);
	}).endAngle(function(d) {
		return directionScale(d.direction - 10);
	});

	// this part scale the transparency of the wings
	var idmax = d3.max(json.records, function(d) {
		return d.id;
	});
	var idScale = d3.scale.linear().domain([0, idmax]).range([0, 1]);

	// main windrose
	var circles = vis.selectAll("circle").data(SPEED_CIRCLES).enter().append("circle");
	var circleAttributes = circles.attr("cx", centerX).attr("cy", centerY).attr("r", function(d) {
		return (speedScale(d) + windRoseRadius);
	}).style("stroke", "black").style("stroke-width", 0.25).style("fill", "none");
	vis.selectAll("path").data(json.records).enter().append("path").attr("d", arc).style("stroke", "black").style("stroke-width", 0.5).style("fill", function(d) {
		return "rgb(0," + (d.id * 50) + ", " + (d.id * 10) + ")";
	}).style("fill-opacity", function(d) {
		return (idScale(d.id));
	}).attr("transform", "translate(250,250)").append("svg:title").text(function(d) {
		return d.direction + " deg\n" + d.speed + " m/sec\n" + d.timestamp;
	});

	// adding all stations to the map
	d3.json(stationsJson, function(collection) {
		// setting d3 elements for the leaflet overlayer
		var svg = d3.select(map.getPanes().overlayPane).append("svg");
		var g = svg.append("g").attr("class", "leaflet-zoom-hide");
		var transform = d3.geo.transform({
			point : projectPoint
		});
		var path = d3.geo.path().projection(transform);
		// d3_features for the station locations
		d3_features = g.selectAll("path").data(collection.features).enter().append("path");
		// d3_circles for the windrose scale
		d3_circles = g.selectAll("circle").data(SPEED_CIRCLES).enter().append("circle");
		// d3_arcs for the windrose wings
		d3_arcs = g.selectAll("path").data(json.records).enter().append("path");

		// reset overlays with each map view reset (such as zooming in/out)
		map.on("viewreset", putPointsOnMap);
		putPointsOnMap();

		function putPointsOnMap() {
			bounds = path.bounds(collection);
			var topLeft = bounds[0];
			var bottomRight = bounds[1];
			svg.attr("width", bottomRight[0] - topLeft[0]);
			svg.attr("height", bottomRight[1] - topLeft[1]);
			svg.style("left", topLeft[0] + "px");
			svg.style("top", topLeft[1] + "px");
			g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");

			// put station locations on the map :)
			var windPoints = d3_features.attr("d", path);
			windPoints.attr("r", 500);
			windPoints.style('fill', 'green');
			windPoints.style("stroke", "black");
			windPoints.style("stroke-width", 0.5);
			console.log(collection);
			windPoints.append("svg:title").text(collection, function(d) {
				console.log(d.features.name);
				return d.features.name;
			});

			// put scale circles on the map
			var centerX = projectPointToScreen(lon, lat).x
			var centerY = projectPointToScreen(lon, lat).y
			console.log(centerX, centerY);
			d3_circles.attr("cx", centerX).attr("cy", centerY).attr("r", function(d) {
				return (speedScale(d) + windRoseRadius);
			}).style("stroke", "black").style("stroke-width", 0.5).style("fill", "none");
			console.log(JSON.stringify(projectPointToScreen(lon, lat)));

			d3_arcs.attr("d", arc).attr("cx", centerX).attr("cy", centerY).style("stroke", "black").style("stroke-width", 0.5).style("fill", function(d) {
				return "rgb(0," + (d.id * 50) + ", " + (d.id * 10) + ")";
			}).style("fill-opacity", function(d) {
				return (idScale(d.id));
			});
		}

	});
	// Use Leaflet to implement a D3 geometric transformation.
	function projectPoint(x, y) {
		var point = map.latLngToLayerPoint(new L.LatLng(y, x));
		this.stream.point(point.x, point.y);
	};
	// Use Leaflet to implement a D3 geometric transformation.
	function projectPointToScreen(x, y) {
		var point = map.latLngToLayerPoint(new L.LatLng(y, x));
		return (point);
	};
});
