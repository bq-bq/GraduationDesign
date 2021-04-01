
function _cpp_codemirror_output_from_textarea(textArea, editable, source_type) {
	var source_mode = "text/x-c++src";
	if (source_type == 'Python') {
		source_mode = {name: "python", version: 3, singleLineStringErrors: false};
	}
	return CodeMirror.fromTextArea(textArea, {
		lineNumbers: true,
		lineWrapping: true,
		viewportMargin: Infinity,
		tabSize: 4,
		indentUnit: 4,
		indentWithTabs: true,
		matchBrackets: true,
		mode: source_mode,
		readOnly: true,
	});		
}

function _cpp_codemirror_output_get_text(data, data_column) {
	var text = '';
	if (data != null && 'rows' in data && data['rows'].length > 0) {
		if (data_column < data['rows'][0].length)
			text = data['rows'][0][data_column];
	}
	if (text == null) text = '';
	return text;
}

function cpp_codemirror_output_js() {
	var obj = {
		type_name: 'config_edit_table',
		elt: null,
		event_listener: null,
		config: null,
		source: null,
		output: null,
		title: '运行结果',
		data_column: 0,
 		margin: null,
 		width: null,
 		runable: true,
 		editor: null,
		use_example_data() {
			var example_source = '';
			var rows = [['']];
			for (var i = 0; i < 10; ++ i) rows[0].push(example_source);
			this.source = {'field_names':['source'],'field_types':['text'],'rows':rows};
			this.output = {'field_names':['source'],'field_types':['text'],'rows':rows};
			this._set_data();
		},
		get_data_json_text(data_name) {
			if (data_name == 'source_data') {
				if (this.source == null) return null;
				return JSON.stringify(this.source);
			}
			else if (data_name == 'output') {
				if (this.output == null) return null;
				return JSON.stringify(this.output);
			}
			else {
				error_toast('不存在的数据: ' + data_name);
			}
			return null;
		},
		set_data(data_name, data) {
			if (data_name == 'source') {
				var refresh = ((this.source == null) != (data == null));
				this.source = data;
				if (refresh) this._set_data();
			}
			else if (data_name == 'output') {
				var text1 = _cpp_codemirror_output_get_text(this.output, this.data_column);
				var text2 = _cpp_codemirror_output_get_text(data, this.data_column);
				this.output = data;
				if (text1 != text2) this._set_data();
			}
			else {
				// error_toast('不存在的数据: ' + data_name);
			}
		},
		set_config(config) {
			this.config = config;
			var style = {};
			if ('style' in config) 
				style = config['style'];
			this.margin = null;
			if ('margin' in style)
				this.margin = style['margin'];
			this.width = null;
			if ('width' in style)
				this.width = style['width'];
			this.data_column = 0;
			if ('data_column' in config['attr'])
				this.data_column = parseInt(config['attr']['data_column']);
			this.source_type = 'cpp';
			if ('source_type' in config['attr'])
				this.source_type = config['attr']['source_type'];
			this.title = '运行结果'
			if ('title' in config['attr'])
				this.title = config['attr']['title'];
			this.runable = true;
			if ('runable' in config['attr'])
				this.runable = (config['attr']['runable'] == 'True');
			this._set_data();
		},
		_set_data() {
			$(obj.elt).empty();
			if (this.source == null) return;
			var form = null;
			var style = {};
			if (this.margin != null) style['margin'] = this.margin;
			if (this.width != null) style['width'] = this.width;
			if (this.title != null) {
				var card = $('<div></div>', {'class':'card'}).css(style).appendTo($(this.elt));
				$('<div></div>', {'class':'card-header'}).text(this.title).appendTo(card);
				form = $('<div></div>', {'class':'card-body'}).appendTo(card);
			}
			else {
				form = $('<div></div>').css(style).appendTo($(this.elt));
			}
			var text = _cpp_codemirror_output_get_text(this.output, this.data_column);
			var text_area = $('<textarea></textarea>').appendTo(form);
			var this_ = this;
			function onRun(ev) {
				if (this_.event_listener != null && this_.source != null) {
					// text = '请稍等...'
					// this_.editor.setValue(text);
					if (this_.output != null && this_.output['rows'].length > 0) {
						if (this_.data_column < this_.output['rows'][0].length) {
							this_.output['rows'][0][this_.data_column] = text;
							// this_.event_listener('change', 'output');
						}
					}
					this_.event_listener('change', 'source_data');
					this_.event_listener('run', null);
					show_spinner_modal()
				}
			}
			if (this.editor != null)
				this.dispose();
			this.editor = _cpp_codemirror_output_from_textarea(text_area[0], false, this.source_type);
			this.editor.setValue(text);
			if (this.runable) {
				var run_button = $('<button></button>', {'class':'btn btn-success'}).text('运行').css({'margin':'10px 0px 0px 0px'}).appendTo(form);
				run_button.bind('click', onRun)
			}
		},
		dispose() {
			if (this.editor != null)
				this.editor.toTextArea();
		}
	};
	obj.elt = document.createElement("div");
	return obj;
}

