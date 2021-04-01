
// 这个控件用来显示一个数据库表格的第一行
// <div>
// 	<div class="form-group">
// 		<label for="id_姓名">姓名</label>
// 		<input type="text" class="form-control" id="id_姓名" aria-describedby="姓名">
// 	</div>
// 	<div class="form-group">
// 		<label for="id_电话">电话</label>
// 		<input type="text" class="form-control" id="id_电话" aria-describedby="电话">
// 	</div>
// </div>
// 本例子中包含以下回调函数 set_data, get_data_json_text, get_config, mounted, use_example_data
// 这个回调函数中的每一个如果没有必要是可以忽略不写的

function test_form_js_obj() {
	// 创建一个py对象，代表一个控件
	var obj = {
		// 该对象需要有一个叫elt的文档节点，作为该控件的根节点
		elt: null,
		// 该对象需要有一个config成员，用以存放该控件的设置信息
		config: null,
		// 该对象需要有一个event_listener函数，这个函数将会有网页设置
		// 这个函数用以向网页和其它控件发送该控件的事件
		event_listener: null,
		// 以下是成员用以存放该控件的数据，由每个控件自己定义
		my_data: null,

		// 如果该控件绑定了表格数据，那么当一个名为data_name的表格数据
		// 被改变为data的时候，网页会调用这个set_data函数
		set_data(data_name, data) { // data_name == 'data1'
			this.my_data = data; // 这是一个dict，包含叫field_names和field_types两个list(str)和一个叫rows的list(list(str))
			this._update_component_UI(); // 这个函数后面定义，用来根据新的数据更新控件
		},

		// 如果该控件绑定了表格数据，那么当该控件调用this.event_listener
		// 向网页发送了名字为data_name的表格数据的change事件后，
		// 网页会调用这个get_data_json_text函数获取该控件的该表格数据
		get_data_json_text(data_name) { // data_name == 'data1'
			return JSON.stringify(this.my_data);
		},

		// 在UI应用时，控件的设置可以被UI应用右侧的设置表格修改
		// 控件的设置被修改时，该函数会被调用
		set_config(config) {
			this.config = config; // 这是一个dict，包含三个分别叫attr,style,class的dict
			this._update_component_UI(); // 这个函数后面定义，用来根据新的设置更新控件
		},

		// 某些控件需要在根节点(this.elt)被添加到网页后才能正确构建
		// 该函数会在this.elt被添加到网页后被调用
		// config 同get_config函数的参数
		// is_editing (True/False) 表示当前空间是否在UI应用中被编辑
		// (这允许控件在被编辑状态被显示得不同，通常在编辑状态下控件不易占用太大的空间)
		// 该控件也可以更改自己的config，一但修改需要调用
		// if this.edit_listener is not None: this.edit_listener('edited', None)
		// 以通知UI应用
		mounted(config, is_editing, edit_listener) {
			this.config = config;
			this.edit_listener = edit_listener;
			this._update_component_UI(); // 这个函数后面定义，用来根据设置更新控件
		},

		// 当控件在被编辑状态时，该函数会被调用，以设置该控件在被编辑状态时的数据
		use_example_data() {
			this.my_data = {'field_names':['姓名','电话'],
				'field_types':['text','text'],
				'rows':[['张三','1234567890']]};
			this._update_component_UI() // 这个函数后面定义，用来根据设置更新控件
		},

		_update_component_UI() {
			var config = this.config;
			var data = this.my_data;

			$(this.elt).empty(); // 清空该控件的节点
			if (data == null || config == null) return;
			var form = null;
			if ('width' in config['style']) {
				var width = config['style']['width'];
				form = $('<div style="width:'+width+';"></div>');
			}
			else {
				form = $('<div></div>');
			}
			form.appendTo($(this.elt)); // 添加form控件

			var field_names = data['field_names'];
			var row = data['rows'][0];
			var this_ = this
			function on_change(ev) {
				var input = ev.target;
				var i = parseInt(input.id);
				row[i] = input.value;
				if (this_.event_listener != null)
					this_.event_listener('change', 'data1'); // 通知网页名为'data1'的数据被修改了
			}
			for (var i = 0; i < field_names.length; ++ i) {
				var field_name = field_names[i];
				var form_group = $('<div></div>', {'class':'form-group'});
				$('<label>'+field_name+'</label>').appendTo(form_group);
				var input = $('<input></input>', {'id':''+i, 'type':'text', 'value':row[i], 'class':'form-control', 'aria-describedby':field_name});
				input.bind('blur', on_change); // 这是同名的DOM事件 'blur'
				input.appendTo(form_group);
				form_group.appendTo(form);
			}
		}
	};
	obj.elt = document.createElement("div");
	return obj;
}
