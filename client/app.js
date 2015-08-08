/*
 * Class for generating real-time data for the area, line, and bar plots.
 */
var RealTimeData = function(layers) {
		this.layers = layers;
		this.timestamp = ((new Date()).getTime() / 1000)|0;
};

RealTimeData.prototype.rand = function() {
		return parseInt(Math.random());// + 50;
};

RealTimeData.prototype.history = function(entries) {
		if (typeof(entries) != 'number' || !entries) {
				entries = 60;
		}

		var history = [];
		for (var k = 0; k < this.layers; k++) {
				history.push({ values: [] });
		}

		for (var i = 0; i < entries; i++) {
				for (var j = 0; j < this.layers; j++) {
						history[j].values.push({time: this.timestamp, y: this.rand()});
				}
				this.timestamp++;
		}

		return history;
};

RealTimeData.prototype.next = function() {
		var entry = [];
		for (var i = 0; i < this.layers; i++) {
				entry.push({ time: this.timestamp, y: this.rand() });
		}
		this.timestamp++;
		return entry;
}

var data = new RealTimeData(2);
var foo = data.next();

var chart = $('#real-time-line').epoch({
		type: 'time.line',
		data: [{values: [foo[0]]}, {values: [foo[1]]}],
		axes: ['left', 'bottom', 'right']
});


setInterval(function() {
	$.get("http://localhost:5000/api/", function(data) {
		chart.push(data.data);
	})
}, 100);
chart.push(data.next());
