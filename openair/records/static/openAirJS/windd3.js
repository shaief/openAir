var map = L.map('map').setView([lat, lon], 16);
L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg', {
	attribution : 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
	subdomains : 'abcd',
	minZoom : 3,
	maxZoom : 16
	// L.tileLayer('http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
	// attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
	// subdomains: 'abcd',
	// minZoom: 3,
	// maxZoom: 16
	// L.tileLayer('http://{s}.tile.cloudmade.com/8897a64b9ba14c60ac9fa07924a23e40/997/256/{z}/{x}/{y}.png', {
	// attribution : 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
	// maxZoom : 18
}).addTo(map);

// constants
var centerX = 250;
var centerY = centerX;
var SPEED_CIRCLES = [0, 2, 4, 6, 8, 10];
var windRoseRadius = 10;

// d3 scales
var speedColorScale = d3.scale.category20c().domain([0, 50]);
var directionScale = d3.scale.linear().domain([0, 360]).range([0, 2 * Math.PI]);
var speedScale = d3.scale.linear().domain([0, 100]).range([0, 1500]);

// calling json for station's windrose
var data = d3.json(windJson, function(error, json) {
	if (error)
		return console.warn(error);
	var windrose_json = json.records;
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
	var idmax = d3.max(json.records, function(windrose_json) {
		return windrose_json.id;
	});
	var idScale = d3.scale.linear().domain([0, idmax]).range([0, 1]);

	// // main windrose
	// var circles = vis.selectAll("circle").data(SPEED_CIRCLES).enter().append("circle");
	// var circleAttributes = circles.attr("cx", centerX).attr("cy", centerY).attr("r", function(d) {
	// return (speedScale(d) + windRoseRadius);
	// }).style("stroke", "black").style("stroke-width", 0.25).style("fill", "none");
	// vis.selectAll("path").data(json.records).enter().append("path").attr("d", arc).style("stroke", "black").style("stroke-width", 0.5).style("fill", function(d) {
	// return "rgb(0," + (d.id * 50) + ", " + (d.id * 10) + ")";
	// }).style("fill-opacity", function(d) {
	// return (idScale(d.id));
	// }).attr("transform", "translate(" + centerX + "," + centerY + ")").append("svg:title").text(function(d) {
	// return d.direction + " deg\n" + d.speed + " m/sec\n" + d.timestamp;
	// });

	// adding all stations to the map
	var data_stations = d3.json(stationsJson, function(error, collection) {
		if (error) return console.warn(error);
		stations_json = [collection.features];
		var stations_json_features = stations_json[0];
		console.log(stations_json);
                  console.log(stations_json[0]);
                  console.log(stations_json[0][0]);
                  console.log(stations_json[0][0].geometry);
                  console.log(stations_json[0][0].geometry.coordinates);
		// setting d3 elements for the leaflet overlayer
		var svg = d3.select(map.getPanes().overlayPane).append("svg");
		var g = svg.append("g").attr("class", "leaflet-zoom-hide");
		var transform = d3.geo.transform({
			point : projectPoint
		});
		var path = d3.geo.path().projection(transform);
		// d3_features for the station locations
		d3_features = g.selectAll("path.points").data(collection.features).enter().append("path");

		// reset overlays with each map view reset (such as zooming in/out)
		map.on("viewreset", putPointsOnMap);
		putPointsOnMap();

                  map.on("dragend", mapMoved);

                function mapMoved(){
                    console.log("center: " + map.getCenter());
                    var mapCenter = map.getCenter();
                    console.log("array length: " + stations_json_features.length);
                    var sortable = [];
                    for (var sta = 0; sta < stations_json_features.length; sta++){
                        var pLat = stations_json_features[sta].geometry.coordinates[0];
                        var pLon = stations_json_features[sta].geometry.coordinates[1]
                        var station_url_id =  stations_json_features[sta].url_id;
                        var zone_url_id = stations_json_features[sta].zone_url_id;
                        var dist = mapCenter.distanceTo(new L.latLng(pLon, pLat));
                        console.log("sta "+ sta + " url " + station_url_id + " dist "+ dist);
                        sortable.push([sta, zone_url_id, station_url_id, pLon, pLat, dist]);
                        };
                    sortable.sort(function(a, b) {
                        return (a[5]-b[5]);
                        });
                    console.log("closest point: " + sortable[0]);
                    console.log(windUrl);
                    var newWindJson = windUrl + sortable[0][2];
                    var data = d3.json(newWindJson);
                    var windrose_json = json.records;
                    };

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
			windPoints.append("a").attr("xlink:href", function(stations_json) {
				return (stations_url + "/" + stations_json.zone_url_id + "/" + stations_json.url_id + "/");
			});
			windPoints.attr("r", 500);
			windPoints.style('fill', 'green');
			windPoints.style("stroke", "black");
			windPoints.style("stroke-width", 0.5);
			windPoints.append("svg:title").text(function(stations_json) {
				return stations_json.name;
			});
			

			var windroseX = projectPointToScreen(lon, lat).x;
			var windroseY = projectPointToScreen(lon, lat).y;
			
			console.log("map zoom: " + map.getZoom());
			// remove scale circles from the map
			if (map.getZoom() < 16) {
				console.log("zooming out")
				d3_circles.remove();
				d3_arcs.remove();
			}
			if (map.getZoom() > 15) {
				// d3_circles for the windrose scale
				// put scale circles on the map
				d3_circles = g.selectAll("circle").data(SPEED_CIRCLES).enter().append("circle");
				// d3_arcs for the windrose wings
				d3_arcs = g.selectAll("path.arcs").data(json.records).enter().append("path");

				d3_circles.attr("cx", windroseX).attr("cy", windroseY).attr("r", function(windrose_json) {
					return (speedScale(windrose_json) + windRoseRadius);
				}).style("stroke", "green").style("stroke-width", 1).style("fill", "none");
				console.log(JSON.stringify(projectPointToScreen(lon, lat)));

				d3_arcs.attr("d", arc).attr("transform", "translate(" + windroseX + "," + windroseY + ")").style("stroke", "black").style("stroke-width", 0.5).style("fill", function(d) {
					return "rgb(0," + (d.id * 50) + ", " + (d.id * 10) + ")";
				}).style("fill-opacity", function(windrose_json) {
					return (idScale(windrose_json.id));
				}).append("svg:title").text(function(windrose_json) {
					return windrose_json.direction + " deg\n" + windrose_json.speed + " m/sec\n" + windrose_json.timestamp;
				});

			}

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
