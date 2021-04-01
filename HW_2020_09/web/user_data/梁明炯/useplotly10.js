function mingjiong_plotly2_js() {
	var obj = {
		elt: document.createElement("div"),
		event_listener: null,
		config: null,
		source: null,
		output: null,
		title: 'plotly',
 		margin: null,
 		width: null,
 		runable: true,
		use_example_data() {
			this._set_data();
			
		},
		set_data(data_name, data) {
		},
		set_config(config) {
			this._set_data();
		},
		_set_data() {
			$(obj.elt).empty();
			startPlotly(obj.elt);
		}
	};

	return obj;
}


function startPlotly(div)
{
	var trace1 = {
	  x: ['giraffes', 'orangutans', 'monkeys'],
	  y: [20, 14, 23],
	  name: 'SF Zoo',
	  type: 'bar'
	};

	var trace2 = {
	  x: ['giraffes', 'orangutans', 'monkeys'],
	  y: [12, 18, 29],
	  name: 'LA Zoo',
	  type: 'bar'
	};

	var data = [trace1, trace2];

	var layout = {barmode: 'stack'};

	Plotly.newPlot(div, data, layout);
}
