var Dygraph = require('dygraphs')

new Dygraph(document.getElementById("viz"),
						[
							[1,10,100],
							[2,20,80],
							[3,50,60],
							[4,70,80]
						],
						{
							labels: ["x", "A", "B"]
						});

var data = [];
var t0 = new Date();
var getx = function(t) {
	return Math.sin(0.001*t) + 0.5*Math.random() - 0.25;
}
for (var i = 1000; i >= 0; i--) {
	var t = new Date(t0.getTime() - i * 10);
	data.push([t, getx(t)]);
}

var g = new Dygraph(document.getElementById("live"),
									 data,
									 {
										 drawPoints: false,
										 showRoller: true,
										 valueRange: [-1.4, 1.4],
										 labels: ['t', 'v(t)']
									 })

window.setInterval(function() {
	var t = new Date();
	data.push([t,getx(t)]);
	data.shift()
	g.updateOptions({'file': data});
}, 10);
