
function _cpp_codemirror_init() {
	CodeMirror.commands.autocomplete = function(cm) {
		cm.showHint({hint: CodeMirror.hint.anyword});
	}

	var WORD = /[\w$]+/, RANGE = 500;
	var c_keywords = [
		"for (int i = 0; i < ; ++ i) ",
		"for ",
		"if ",
		"using namespace std;",
		"using ",
		"namespace ",
		"std",
		"include <iostream>",
		"include <string>",
		"include ",
		"while ",
		"do ",
		"switch ",
		"default",
		"case:",
		"continue;",
		"break;",
		"struct ",
		"class ",
		"this->",
		"this",
		"private:",
		"public:",
		"protected:",
		"static ",
		"int ",
		"float ",
		"double ",
		"char ",
		"string ",
		"cin >> ",
		"cout << ",
		"cout << ",
		"endl;",
		"main() {\n\t\n}"
		];
	function get_hint_list(editor, options) {
		var word = options && options.word || WORD;
		var range = options && options.range || RANGE;
		var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
		var end = cur.ch, start = end;
		while (start && word.test(curLine.charAt(start - 1))) --start;
		var curWord = start != end && curLine.slice(start, end);

		var list = [];
		var seen = {};
		var re = new RegExp(word.source, "g");
		for (var dir = -1; dir <= 1; dir += 2) {
			var line = cur.line, endLine = Math.min(Math.max(line + dir * range, editor.firstLine()), editor.lastLine()) + dir;
			for (; line != endLine; line += dir) {
				var text = editor.getLine(line), m;
				while (m = re.exec(text)) {
					if (line == cur.line && m[0] === curWord) continue;
					if ((!curWord || m[0].lastIndexOf(curWord, 0) == 0) && !Object.prototype.hasOwnProperty.call(seen, m[0])) {
						seen[m[0]] = true;
						list.push(m[0]);
					}
				}
			}
		}
		for (var i = 0; i < c_keywords.length; ++ i) {
			c_keyword = c_keywords[i];
			if (c_keyword.startsWith(curWord) && list.indexOf(c_keyword) === -1)
				list.push(c_keyword);
		}
		if (list.length == 1) list.push('');
		return {list: list, from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end)};
	}
	CodeMirror.registerHelper("hint", "text/x-c++src", get_hint_list);
}

_cpp_codemirror_init();


function _cpp_codemirror_from_textarea(textArea, editable, onSave, source_type) {
	// textArea.addEventListener("save", function(event){
	//	event.preventDefault()
	// });
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
		autoCloseBrackets: true,
		theme: editable?"blackboard":"default",
		readOnly: !editable,

		extraKeys: {
			// "Alt": "autocomplete",
			// "Esc": function(cm) {
			// 	cm.setOption("fullScreen", !cm.getOption("fullScreen"));
			// },
			"Ctrl-S": function(cm) { if (onSave != null) onSave(); },
			"Cmd-S": function(cm) { if (onSave != null) onSave(); },
		},
	});		
}

function cpp_codemirror_js() {
	var obj = {
		type_name: 'config_edit_table',
		elt: null,
		event_listener: null,
		config: null,
		data: null,
		title: '代码编辑框',
		data_column: 0,
 		source_type: 'cpp',
 		margin: null,
 		width: null,
 		editable: false,
 		save_button: false,
 		editor: null,
		use_example_data() {
			var example_source = '#include <iostream>\nusing namespace std;\n\nint main() {\n\tcout << "Hello";\n}';
			if (this.source_type == 'Python')
				example_source = 'print("Hello")';
			var rows = [[]];
			var field_names = [];
			var field_types = [];
			for (var i = 0; i < 10; ++ i) {
				rows[0].push(example_source);
				field_names.push('source');
				field_types.push('text');
			}
			this.data = {'field_names':field_names,'field_types':field_types,'rows':rows};
			this._set_data();
		},
		get_data_json_text(data_name) {
			if (this.data == null) return null;
			return JSON.stringify(this.data);
		},
		set_data(data_name, data) {
			this.data = data;
			this._set_data();
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
				this.title = this.source_type+' 编辑框';
			if ('title' in config['attr'])
				this.title = config['attr']['title'];
			this.editable = true;
			if ('editable' in config['attr'])
				this.editable = (config['attr']['editable'] == 'True');
			this.save_button = true;
			if ('save_button' in config['attr'])
				this.save_button = (config['attr']['save_button'] == 'True');
			this._set_data();
		},
		_set_data() {
			if (this.data == null) {
				$(obj.elt).empty();
				return;
			}
			if (this.editor != null) {
				var old_text = this.editor.getValue();
				if (old_text == text) return;
				this.dispose();
			}
			$(obj.elt).empty();
			var rows = this.data['rows']
			var text = null;
			if (rows.length > 0 && this.data_column < rows[0].length && this.data['field_types'][this.data_column] == 'text')
				text = rows[0][this.data_column];
			if (text == null) return;
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
			var text_area = $('<textarea></textarea>').appendTo(form);
			var this_ = this;
			function onSave(ev) {
				if (! this_.editable) return;
				var value = this_.editor.getValue();
				if (rows[0][this_.data_column] == value) return;
				rows[0][this_.data_column] = value;
				if (this_.event_listener != null)
					this_.event_listener('change', 'data');
			}
			var save_version_count = 0;
			function onSaveDelay() {
				save_version_count += 1
				var save_version = save_version_count;
				function callback() {
					// console.log('onSaveDelay', save_version == save_version_count);
					if (save_version == save_version_count) onSave(null);
				}
				setTimeout(callback, 2000);
			}
			this.editor = _cpp_codemirror_from_textarea(text_area[0], this.editable, onSave, this.source_type);
			this.editor.setValue(text);
			if (this.editable && this.save_button) {
				var save_button = $('<button></button>', {'class':'btn btn-primary'}).text('保存').css({'margin':'10px 0px 0px 0px'}).appendTo(form);
				save_button.bind('click', onSave)
			}

			if (this.editable) {
				this.editor.on("inputRead", function(editor, change) {
					if (this_.source_type == 'C++') {
						if (/^[a-zA-Z]+$/.test(change.text))
							this_.editor.showHint(null, { completeSingle: false });
					}
					// if (! this_.save_button) onSaveDelay();
				});
				if (! this_.save_button) {
					// this.editor.on("keyup", function(editor, change) {
					// 	if (change.keyCode == 8 || change.keyCode == 46)
					// 		onSaveDelay();
					// });
					this.editor.on("blur", function(editor, change) {
						onSave(null);
					});
				}
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

