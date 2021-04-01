
function mingjiong_Scatter_js() {
	var obj = {
		elt: document.createElement("div"),
		event_listener: null,
		data: {'rows':[[1,12],[2,9],[7,8],[5,4]]},
		config: null,

		editable: 'True',
		x_label: 'x axis',
		y_label: 'y axis',
		number_of_lines: 1,
		title: 'scatter',
		mode:'markers',
		isFirstX: 'True',

		use_example_data() {
			this._set_data();
		},
		set_data(data_name, data) {
			this.data = data;
			this._set_data();
		},
		set_config(config) {
			this.config = config;

			if ('editable' in config['attr'])
				this.editable = config['attr']['editable'];
			if ('图例标题' in config['attr'])
				this.title = config['attr']['图例标题'];
			if ('横坐标标题' in config['attr'])
				this.x_label = config['attr']['横坐标标题'];
			if ('纵坐标标题' in config['attr'])
				this.y_label = config['attr']['纵坐标标题'];
			if ('数据数目(组)' in config['attr'])
				this.number_of_lines = config['attr']['数据数目(组)'];
			if ('样式' in config['attr'])
				this.mode = config['attr']['样式'];
			if ('使用第一列作为横坐标数据' in config['attr'])
				this.isFirstX = config['attr']['使用第一列作为横坐标数据'];

			this._set_data();
		},
		_set_data() {
			$(obj.elt).empty();
			startPlotly(obj.elt, obj.data, obj.editable, obj.title, obj.x_label, obj.y_label, obj.number_of_lines, obj.mode, obj.isFirstX);
		}
	};

	return obj;
}


function startPlotly(div, data, editable, title, x_label, y_label, number_of_lines, mode, isFirstX)
{
	number_of_lines = parseInt(number_of_lines);
	if(number_of_lines>5)
	{
		error_toast("最多生成5组数据");
		return;
	}
	var len = data['rows'].length;
	if(len==0)
	{
		error_toast("未绑定表格或者表格无数据");
		return;
	}
	var columnLen = data['rows'][0].length;
	if(columnLen<2)
	{
		error_toast("表格数据至少需要2列");
		return;
	}

	var x_dataSet = new Array();
	var y_dataSet = new Array();
	var dataNameSet = new Array();

	console.log('---->div', div);
	console.log('---->number_of_lines', number_of_lines);
	console.log('---->columnLen', columnLen);
	if(isFirstX=='True')
	{
		if(number_of_lines>(columnLen-1))   //例如5列的数据表，最多画4组数据
		{
			error_toast("使用第一列作为横坐标数据时，本数据表最多有"+(columnLen-1)+"组数据");
			return;
		}
		for(var i=0;i<columnLen;i++)
		{
			x_dataSet[i]=0;   //所有横坐标为0(第1列)
			y_dataSet[i]=i+1; //纵坐标为1,2,3....（第2，3，4列）
			dataNameSet[i]='(第1列, 第'+(i+2)+'列)';
		}
	}
	else
	{
		if(number_of_lines>parseInt(columnLen)/2)   //例如5列的数据表，最多画2组数据
		{
			error_toast("使用奇数列作为横坐标数据，偶数列作为纵坐标数据时，本数据表最多有"+(parseInt(columnLen/2))+"组数据");
			return;
		}
		for(var i=0;i<columnLen;i++)
		{
			x_dataSet[i]=i*2;   //横坐标为0,2,4....(第1/3/5..列)
			y_dataSet[i]=i*2+1; //纵坐标为1,3,5....（第2，4，6列）
			dataNameSet[i]='(第'+(i*2+1)+'列, 第'+(i*2+2)+'列)';
		}
	}

	var colors = ['rgb(255, 97, 0)','rgb(0, 255, 0)','rgb(0, 0, 255)','rgb(255, 0, 0)','rgb(131, 19, 139)'];
	var plotlyData = new Array();
	for(var j=0;j<number_of_lines;j++)
	{
		var x_index = x_dataSet[j];
		var y_index = y_dataSet[j];

		var xdata =new Array();
		var ydata =new Array();
		for (var i=0;i<len;i++)
		{ 
			var row = data['rows'][i];
			if(isNaN(parseFloat(row[x_index])) || isNaN(parseFloat(row[y_index]))){
				error_toast('第' + (i+1)+"行存在非数字内容");
				return;
			}
			xdata[i] = parseFloat(row[x_index]);
			ydata[i] = parseFloat(row[y_index]);
		}
		var trace = {
		  x: xdata,
		  y: ydata,
		  mode: mode,
		  line: {
			color: colors[j]
		  },
		  name: dataNameSet[j],
		  type: 'scatter'
		};

		plotlyData[j] = trace;

	}


	var layout = {
		title: title,
		xaxis: {title: x_label},
		yaxis: {title: y_label}
	};

	Plotly.newPlot(div, plotlyData, layout, {displayModeBar: false});
}
