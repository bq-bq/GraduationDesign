/*
elt
mounted(config)
distroy()
event_listener
set_data(data_name, data)
get_data_json_text(data_name)
set_var(var_name, var_)
get_var(var_name)
*/

function parseValue(text, parseFunc, default_value) {
  var val = parseFunc(text);
  if (isNaN(val)) return default_value;
  return val;
}

var sym_str = '~!@#$%^&*()-+={}[]|\\:;"\'<>,.?/　＿～！＠＃＄％＾＆×（）－＋＝｛｝〔〕｜＼：；〃′＜＞，。？／║‖、‘’￥《》㎡²“”＊．·△'
var sym_set = new Set()
for (var i = 0; i < sym_str.length; ++ i)
	sym_set.add(sym_str[i])

function is_identifier(name) {
	name = name.trim()
	if (name.length == 0) return false;
	for (var i = 0; i < name.length; ++ i) {
		if (sym_set.has(name[i])) return false;
		if (i == 0 && name[i] >= '0' && name[i] <= '9') return false;
	}
	return true;
}

function database_schema_svg() {
  var obj = {
    type_name: 'database_schema',
    data: {},
    selected_tablename: null,
    editable: true,
    elt: null,
    event_listener: null,
    svg: null,
    font_size: 13,
    text_margin: 2,
    node_margin: 20,
    selected_object: null, // isDraging == (selected_object != null)
    selected_field: null,
    context_menu: null,
    is_draging: false,
    selected_pos: null,
    mouse_moved: false,
    svg_width: 100,
    svg_height: 100,
    nodes: [],  

    use_example_data() {
      this.data = {
        "表1": {
          "field_names": [
              "表项1",
              "表项2"
          ],
          "field_types": [
              "text",
              "text"
          ],
          "foreign_keys": {},
          "posX": 10,
          "posY": 10,
          "primary_keys": [],
          "table_name": "db1",
          "table_type": ""
        }
      }
    },
    mounted(config, is_editing, edit_listener) {
      this.editable = parseValue(config.attr.editable, Boolean, this.editable);
      this.font_size = parseValue(config.style.font_size, parseInt, this.font_size);
      this.text_margin = parseValue(config.style.text_margin, parseInt, this.text_margin);
      this.node_margin = parseValue(config.style.node_margin, parseInt, this.node_margin);
      $(this.elt).empty();
      this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      // svg.setAttribute('style', 'border: 1px solid black');
      this.svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
      this.elt.oncontextmenu = () => { return false; }
      this.elt.appendChild(this.svg);
      var this_ = this
      this.elt.onmousedown = (ev) => { this_.mousedown(ev); }
      this.elt.onmousemove = (ev) => { this_.mousemove(ev); }
      this.elt.onmouseup = (ev) => { this_.mouseup(ev); }
      this.elt.onmouseleave = (ev) => { this_.mouseleave(ev); }
      this._set_data(this.data)
    },
    distroy() {
      return;
    },
    get_data_json_text(data_name) {
      var data = null;
      if (data_name == 'data') {
        data = this.data
      }
      else {
        if (this.selected_tablename != null) {
          data = {'field_names':['NO_NAME'], 'field_types':['text'], 'rows':[[this.selected_tablename]]}
        }
      }
      if (data == null) return null;
      return JSON.stringify(data);
    },
    set_data(data_name, data) {
      if (data_name == 'data') {
        this._set_data(data)
      }
      else {
        this._set_select(data)
      }
    },
    _set_select(data) { 
      if (data == null) {
        this.selected_tablename = null
      }
      else {
        this.selected_tablename = data['rows'][0][0]
      }
    },

    _disabledEvent(event){
      event = event || window.event;
      if (event.stopPropagation)
        event.stopPropagation();
      event.cancelBubble = true;
      event.preventDefault();
      return false;
    },

    mousedown(event) {
      var x = event.offsetX;
      var y = event.offsetY;
      if (this.editable && this.context_menu != null) {
        if (x >= this.context_menu.x && y >= this.context_menu.y &&
            x < this.context_menu.x + this.context_menu.node_width &&
            y < this.context_menu.y + this.context_menu.node_height) {
          var item_height = this.font_size + this.text_margin;
          var y_offset = y - this.context_menu.y;
          var k = Math.floor((y_offset - this.text_margin) / item_height);
          if (k >= 0 && k < this.context_menu.menu.length) {
              var action = this.context_menu.menu[k];
              switch (action) {
              case '添加表格': this._add_table(x, y); break;
              case '设置表格类型': this._set_table_type(); break;
              case '删除表格': this._remove_table(); break;
              case '重命名表格': this._rename_table(); break;
              case '添加第一个表项': this._add_first_field(); break;
              case '删除表项': this._remove_field(); break;
              case '上移表项': this._move_field_up(); break;
              case '添加下一个表项': this._add_next_field(); break;
              case '重命名表项': this._rename_field(); break;
              case '设置表项类型': this._set_field_type(); break;
              case '设置/取消主键': this._toggle_primary_key(); break;
              case '设置/取消外键': this._set_foreign_key(); break;
              }
          }
          // return this._disabledEvent(event);
          return;
        }
      }
      this._remove_context_menu();
      this.context_menu = null;
      this.selected_pos = [x, y];
      this.selected_object = null;
      this.selected_field = null;
      this.is_draging = false;
      if (this.nodes == null) return;
      for (var i = 0; i < this.nodes.length; ++ i) {
        for (var j = 0; j < this.nodes[i].length; ++ j) {
          var node = this.nodes[i][j];
          if (x >= node.posX && x <= node.posX + node.node_width && y >= node.posY && y <= node.posY + node.node_height) {
            this.selected_object = node;
            this.mouse_moved = false;
            var y_offset = y - node.posY;
            var title_height = this.font_size + this.text_margin * 3 + 1;
            if (y_offset < title_height) this.selected_field = -1;
            else this.selected_field = Math.floor((y_offset - title_height - 0.5 * this.text_margin) / (this.font_size + this.text_margin));
            if (this.selected_field == node.field_names.length) this.selected_field = node.field_names.length - 1;
            // console.log(this.selected_field);
          }
        }
      }
      if (event.which == 1) {
        this.is_draging = (this.selected_object != null);
      }
      else if (this.editable && event.which == 3) {
        // if (this.selected_object != null)
        //   if (this.event_listener != null)
        //       this.event_listener('select', this.selected_object.table_name);
        this.is_draging = false;
        this._show_menu();
        if (this.selected_object != null) {
          if (this.selected_field != null && this.selected_field != -1)
            this.selected_object.rects[this.selected_field].setAttribute('fill-opacity', "0.3");
        } 
      }
      // return this._disabledEvent(event);
      return;
    },

    _prompt(message, match, action) {
      var image = null;
      var inputs=[{'type':'text', 'id':'input_text', 'placeholder':''}];
      var this_ = this;
      function callback(d) {
        d = d[0].trim();
        // if (d == '') {
        //   error_toast('No input.');
        //   return;
        // }
        if (match != null) {
          if (typeof match === "function") {
            if (! match(d)) {
              error_toast('所输入的内容不符合要求: ' + d);
              return;
            }
          }
          else if (match.constructor == Array) {
          	if (match.indexOf(d) == -1) {
          	  error_toast('所输入的内容在给定范围内: ' + d);
          	  return;
          	}
          }        	
        }
        else {
          if (! is_identifier(d)) {
            error_toast('名字中不能包含空格或符号: ' + d);
            return;
          }
        }
        action(d);
      }
      data_modal(image, message, inputs, 'OK', callback);
    },
    _prompt_for_table_type(message, callback) {
      this._prompt(message, ['','client','public','big'], callback);
    },
    _prompt_for_table_name(message, callback) {
      var this_ = this;
      var nodes = this._get_node_list();
      function callback2(table_name) {
        for (var k in nodes) {
          if (nodes[k].table_name == table_name) {
            error_toast('表格 "' + table_name + '" 已经存在.');
            return;
          }
        }
        callback(table_name);
      }
      this._prompt(message, null, callback2);
    },
    _prompt_for_field_name(message, callback) {
      var this_ = this;
      var selected_object = this.selected_object
      this._prompt(message, null, field_name => {
       var field_names = selected_object.field_names;
        if (field_names.indexOf(field_name) != -1) {
          error_toast('表项 "' + field_name + '" 已经存在于表格 "' + 
            selected_object.table_name + '" .');
          return;
        }
        callback(field_name);
      });
    },
    _prompt_for_field_type(message, callback) {
      var this_ = this;
      var selected_object = this.selected_object
      var valid_types = ['text', 'number', 'boolean', 'time' ];
      this._prompt(message, valid_types, field_type => {
        if (valid_types.indexOf(field_type) == -1) {
          error_toast('不正确的表项类型 "' + field_type + '".');
          return;
        }
        callback(field_type);
      });
    },
    _add_table(x, y) {
      var this_ = this;
      this._prompt_for_table_name('请输入新表格的名字', table_name => {
        table_name = table_name.toLowerCase()
        var new_table = {
          "field_names": [],
          "field_types": [],
          "foreign_keys": {},
          "primary_keys": [],
          "table_name": table_name,
          "posX": x,
          "posY": y
        };
        this_.data[table_name] = new_table;
        this_._set_data(this_.data, true);
        if (this.event_listener != null)
          info_toast('已添加表格: '+table_name);
      });
    },
    _remove_table() {
      var this_ = this;
      var table_name = this.selected_object.table_name;
      var nodes = this._get_node_list();
      confirm_modal('请确认删除表格: ' + table_name, ()=> {
        for (var k in nodes) {
          for (var fk in nodes[k].foreign_keys) {
            if (nodes[k].foreign_keys[fk][0] == table_name)
              delete nodes[k].foreign_keys[fk];
          }
        }
        delete this_.data[table_name]
        if (this.event_listener != null) {
          this.event_listener('delete', table_name);
          info_toast('已删除表格: '+table_name);
        }           
        this_._set_data(this_.data, true);
        if (this_.selected_tablename == table_name) {
          this_.selected_tablename = null;
          if (this.event_listener != null) {
            this.event_listener('change', 'select');          
          }
        }
      });
    },
    _rename_table() {
      var this_ = this;
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      this._prompt_for_table_name('请为表格 "' + selected_object.table_name + '" 输入一个新的名字', table_name=> {
        table_name = table_name.toLowerCase()
        var old_name = selected_object.table_name;
        if (old_name == table_name) {
          error_toast('所输入的名字与表格原来的名字一样');
          return;
        }
        var table = this_.data[old_name];
        delete this_.data[old_name];
        if (this.event_listener != null)
          this.event_listener('delete', old_name);
        table['table_name'] = table_name;
        this_.data[table_name] = table;
        for (var k in nodes) {
          for (var fk in nodes[k].foreign_keys) {
            if (nodes[k].foreign_keys[fk][0] == old_name)
              nodes[k].foreign_keys[fk][0] = table_name;
          }
        }
        this_._set_data(this_.data, true);
        if (this.event_listener != null)
          info_toast('已保存表格名字更改: '+old_name+" -> "+table_name);
      });
    },
    _set_table_type() {
      var this_ = this;
      var selected_object = this.selected_object;
      this._prompt_for_table_type('请为表格 "'+selected_object.table_name+'" 输入新的类型:<br>普通表格/[空], 客户表格/client, 公共表格/public, 特大表格/big', table_type=> {
        var old_table_type = '';
        if ('table_type' in selected_object)
          old_table_type = selected_object.table_type;
        if (old_table_type == table_type) {
          info_toast('表格类型没变化');
          return;
        }
        var table = this_.data[selected_object.table_name];
        table.table_type = table_type;
        this_._set_data(this_.data, true);
        if (this.event_listener != null)
          info_toast('表格 "'+selected_object.table_name+'" 的类型已修改为: '+table_type);
      });
    },
    _add_first_field() {
      var this_ = this;
      var selected_object = this.selected_object;
      this._prompt_for_field_name('请为表格 "' + selected_object.table_name + '" 输入第一个表项', field_name => {
        if (this.event_listener != null) 
          this.event_listener('delete', selected_object.table_name);                    
        var table = this_.data[selected_object.table_name]; 
        table.field_names.unshift(field_name)
        table.field_types.unshift('text')
        this_.selected_tablename = null; // ADD: 2020-03-29
        if (this.event_listener != null) {
          this.event_listener('change', 'select');          
        }
        this_._set_data(this_.data, true);
        if (this.event_listener != null) 
          info_toast('已添加第一个表项: '+selected_object.table_name+'.'+field_name);
      });
    },
    _move_field_up() {
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      if (this.event_listener != null)
        this.event_listener('delete', selected_object.table_name);
      for (var k in nodes) {
        if (nodes[k].table_name == selected_object.table_name) {
          var field_name = nodes[k].field_names[this.selected_field];
          var field_type = nodes[k].field_types[this.selected_field];
          nodes[k].field_names[this.selected_field] = nodes[k].field_names[this.selected_field - 1];
          nodes[k].field_types[this.selected_field] = nodes[k].field_types[this.selected_field - 1];
          nodes[k].field_names[this.selected_field - 1] = field_name;
          nodes[k].field_types[this.selected_field - 1] = field_type;
          if (this.event_listener != null) {
            this.event_listener('change', 'select');          
          }
          this._set_data(this.data, true);
          if (this.event_listener != null) 
            info_toast('已上移表项: '+selected_object.table_name+'.'+field_name);
          break;
        }
      }
    },
    _get_node_list() {
      var nodes = [];
      for (let table_name in this.data) {
        if (table_name == '__update_time__') continue;
        nodes.push(this.data[table_name]);
      }
      return nodes;
    },
    _remove_field() {
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      var remove_pos = this.selected_field;
      var this_ = this;
      var field_name = null;
      var node = null;
      for (var k in nodes) {
        if (nodes[k].table_name == selected_object.table_name) {
          field_name = nodes[k].field_names[remove_pos];
          node = nodes[k];
          break;
        }
      }
      confirm_modal('请确认删除表项: ' + selected_object.table_name + '.' + field_name, () => {
        if (this.event_listener != null)
          this.event_listener('delete', selected_object.table_name);                    
        node.field_names.splice(remove_pos, 1);
        node.field_types.splice(remove_pos, 1);
        var pk_index = node.primary_keys.indexOf(field_name);
        if (pk_index != -1)
          node.primary_keys.splice(pk_index, 1);
        for (var k2 in nodes) {
          for (var fk in nodes[k2].foreign_keys) {
            var link = nodes[k2].foreign_keys[fk];
            if (link[0] == selected_object.table_name && link[1] == field_name) {
              delete nodes[k2].foreign_keys[fk];
            }
          }
        }
        this.selected_tablename = null; // ADD: 2020-03-29
        if (this.event_listener != null) {
          this.event_listener('change', 'select');          
        }
        this_._set_data(this_.data, true);
        if (this.event_listener != null)
          info_toast('已删除表项: '+selected_object.table_name+'.'+field_name);
      });
    },
    _add_next_field() {
      var this__ = this;
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      var insert_pos = this.selected_field + 1;
      this._prompt_for_field_name('请为表格 "' + selected_object.table_name + '" 输入一个表项', field_name => {
        if (this.event_listener != null)
          this.event_listener('delete', selected_object.table_name);                    
        for (var k in nodes) {
          if (nodes[k].table_name == selected_object.table_name) {
            nodes[k].field_names.splice(insert_pos, 0, field_name);
            nodes[k].field_types.splice(insert_pos, 0, 'text');
            this.selected_tablename = null; // ADD: 2020-03-29
            if (this.event_listener != null) {
              this.event_listener('change', 'select');          
            }
            this__._set_data(this__.data, true);
            if (this.event_listener != null)
              info_toast('已添加表项: '+selected_object.table_name+'.'+field_name);
            break;
          }
        }
      });
    },
    _rename_field() {
      var this__ = this;
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      var selected_field = this.selected_field;
      var node = null;
      for (var k in nodes) {
        if (nodes[k].table_name == selected_object.table_name) {
          node = nodes[k];
          break;
        }
      }
      this._prompt_for_field_name('请为表项 "' + selected_object.table_name + '.' + node.field_names[selected_field] + '" 输入一个新的名字', field_name => {
        if (field_name in node.field_names) {
          error_toast('表项名 "' + field_name + '" 已经存在于表格 "' + selected_object.table_name + '"');
          return;
        }
        if (this.event_listener != null)
          this.event_listener('delete', selected_object.table_name);                    
        var old_name = node.field_names[selected_field];
        node.field_names[selected_field] = field_name;
        var pk_index = node.primary_keys.indexOf(old_name);
        if (pk_index != -1)
          node.primary_keys[pk_index] = field_name;
        if (old_name in node.foreign_keys) {
          node.foreign_keys[field_name] = node.foreign_keys[old_name];
          delete node.foreign_keys[old_name];
        }
        for (var k2 in nodes) {
          for (var fk in nodes[k2].foreign_keys) {
            var link = nodes[k2].foreign_keys[fk];
            if (link[0] == selected_object.table_name && link[1] == old_name) {
              link[1] = field_name;
            }
          }
        }            
        this__._set_data(this__.data, true);
        if (this.event_listener != null)
          info_toast('已保存表项更名: '+selected_object.table_name+'.'+old_name + ' -> '+selected_object.table_name+'.'+field_name);
      });
    },
    _set_field_type() {
      var this__ = this;
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      var selected_field = this.selected_field;
      var node = null;
      for (var k in nodes) {
        if (nodes[k].table_name == selected_object.table_name) {
          node = nodes[k];
          break;
        }
      }
      this._prompt_for_field_type('请为表项 "'+selected_object.table_name+'.'+node.field_names[selected_field]+'" 设置表项类型: <br>文本类型/text, 数字类型/number, 真假类型/boolean, or 时间类型/time.', field_type => {
        if (this.event_listener != null)
          this.event_listener('delete', selected_object.table_name);                    
        for (var k in nodes) {
          if (nodes[k].table_name == selected_object.table_name) {
            var old_type = nodes[k].field_types[selected_field];
            nodes[k].field_types[selected_field] = field_type;          
            this__._set_data(this__.data, true);
            if (this.event_listener != null)
              info_toast('已保存表项 "'+selected_object.table_name+'.'+node.field_names[selected_field]+'" 的类型更改: '+old_type + ' -> '+field_type);
            break;
          }
        }
      });
    },
    _toggle_primary_key() {
      var nodes = this._get_node_list();
      var selected_object = this.selected_object;
      for (var k in nodes) {
        if (nodes[k].table_name == selected_object.table_name) {
          var field_name = nodes[k].field_names[this.selected_field];
          var key_index = nodes[k].primary_keys.indexOf(field_name);
          if (key_index == -1)
            nodes[k].primary_keys.push(field_name);
          else
            nodes[k].primary_keys.splice(key_index, 1);
          this._set_data(this.data, true);
          if (this.event_listener != null)
            info_toast('已将 "'+selected_object.table_name+'.'+field_name+'" 设置为 ' + (key_index==-1?'主键':'非主键'));
          break;
        }
      }
    },
    _prompt_for_foreign_key(callback) {
      var this__ = this;
      var selected_object = this.selected_object;
      var nodes = this._get_node_list();
      var check_foreign_key = function(foreign_table, foreign_field) {
        for (var k in nodes) {
          if (nodes[k].table_name == foreign_table) {
            return nodes[k].field_names.indexOf(foreign_field) != -1;
          }
        }
        return false;
      }
      function match(name) {
      	if (name == '.') return true;
      	name = name.split('.')
      	if (name.length != 2) return false;
      	if (! is_identifier(name[0])) return false;
      	if (! is_identifier(name[1])) return false;
      	return true;
      }
      this._prompt('请输入一个外键, 格式: <外表名>.<外键名><br> 如果要删除外键, 请输入一个 "."', match, names => {
        names = names.trim();
        if (names == '.') {
          callback('', '');
          return;
        }
        names2 = names.split('.');
        if (names2.length != 2) {
          error_toast('错误的输入:'+names);
          return;
        }
        var foreign_table = names2[0].trim();
        var foreign_field = names2[1].trim();
        if (! check_foreign_key(foreign_table, foreign_field)) {
          error_toast('不存在外键: "' + foreign_table + '.' + foreign_field + '"');
          return;
        }
        callback(foreign_table, foreign_field);
      });
    },
    _set_foreign_key() {
      var nodes = this._get_node_list();
      var node = null;
      for (var k in nodes) {
        if (nodes[k].table_name == this.selected_object.table_name)
          node = nodes[k];
      }
      var field_name = node.field_names[this.selected_field];
      this._prompt_for_foreign_key((foreign_table, foreign_field) => {
        if (foreign_table == '' && foreign_field == '') {
          if (field_name in node.foreign_keys) {
            foreign_table = node.foreign_keys[field_name][0];
            foreign_field = node.foreign_keys[field_name][1];
            delete node.foreign_keys[field_name];
          }
          else
            return;
        }
        else {
          node.foreign_keys[field_name] = [foreign_table, foreign_field];
        }
        this._set_data(this.data, true);
        if (this.event_listener != null)
          if (field_name in node.foreign_keys)
            info_toast('已添加外键: '+node.table_name+'.'+field_name+' --> '+foreign_table+'.'+foreign_field);
          else
            info_toast('已取消外键: '+node.table_name+'.'+field_name+' --> '+foreign_table+'.'+foreign_field);
      });
    },

    _show_menu() {
      var max = function(x, y) {
        if (x == null) return y;
        if (y == null) return x;
        return x > y ? x : y;
      };
      var min = function(x, y) {
        if (x == null) return y;
        if (y == null) return x;
        return x < y ? x : y;
      };
      var menu = null;
      if (this.selected_field == null)
        menu = [ '添加表格' ];
      else if (this.selected_field == -1)
        menu = [ '删除表格', '重命名表格', '设置表格类型', '添加第一个表项' ];
      else {
        menu = [ '删除表项', '添加下一个表项', '重命名表项', '设置表项类型', '设置/取消主键', '设置/取消外键' ];
        if (this.selected_field != 0)
          menu.unshift('上移表项');
      }
      this.context_menu = {}
      this.context_menu.x = this.selected_pos[0];
      this.context_menu.y = this.selected_pos[1];
      this.context_menu.menu = menu;
      this.context_menu.rects = []
      var node = document.createElementNS("http://www.w3.org/2000/svg", "g");
      this.svg.appendChild(node);
      this.context_menu.node = node;
      var menu_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      menu_rect.setAttribute("x", '0px');
      menu_rect.setAttribute("y", '0px');
      var node_height = (this.font_size + this.text_margin) * menu.length + this.text_margin * 2 + 1
      menu_rect.setAttribute("height", node_height);
      menu_rect.setAttribute("fill", "#FFFFFF");
      menu_rect.setAttribute("fill-opacity", 0.9);
      menu_rect.setAttribute("stroke", "#909399");
      menu_rect.setAttribute("stroke-width", "1");
      node.appendChild(menu_rect);
      var node_width = null;
      for (var k = 0; k < menu.length; ++ k) {
        var text_y = (this.font_size + this.text_margin) * (k + 1);
        var text_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        text_rect.setAttribute("x", '0px');
        text_rect.setAttribute("y", (text_y - this.font_size + this.text_margin) + 'px');
        text_rect.setAttribute("height", this.font_size);
        text_rect.setAttribute("fill", "#909399");
        text_rect.setAttribute("fill-opacity", 0);
        text_rect.setAttribute("stroke-width", "0");
        node.appendChild(text_rect);
        this.context_menu.rects.push(text_rect);
        var menu_text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        menu_text.textContent = menu[k];
        menu_text.setAttribute("font-size", this.font_size);
        menu_text.setAttribute("x", this.text_margin);
        menu_text.setAttribute("y", text_y);
        menu_text.setAttribute("fill", "#000000");
        node.appendChild(menu_text);
        node_width = max(node_width, menu_text.getBBox().width + 2 * this.text_margin);
      }
      menu_rect.setAttribute( "width", node_width);
      for (var k = 0; k < this.context_menu.rects.length; ++ k)
        this.context_menu.rects[k].setAttribute( "width", node_width);
      this.context_menu.node_width = node_width;
      this.context_menu.node_height = node_height;
      this.context_menu.x = min(this.context_menu.x, this.svg_width - node_width);
      this.context_menu.y = min(this.context_menu.y, this.svg_height - node_height);
      node.setAttribute("transform", "translate(" + this.context_menu.x + ", " + this.context_menu.y +")");
    },

    _remove_context_menu() {
      if (this.selected_object != null && this.selected_field != null && this.selected_field != -1)
        this.selected_object.rects[this.selected_field].setAttribute('fill-opacity', "0");
      if (this.context_menu != null)
        this.svg.removeChild(this.context_menu.node);
      this.context_menu = null;
    },

    _updateBounds(update_min_bounds) {
      if (this.nodes == null) return;
      var max = function(x, y) {
        if (x == null) return y;
        if (y == null) return x;
        return x > y ? x : y;
      }
      var min = function(x, y) {
        if (x == null) return y;
        if (y == null) return x;
        return x < y ? x : y;
      }
      var min_x = null;
      var min_y = null;
      var max_x = null;
      var max_y = null;
      for (var i = 0; i < this.nodes.length; ++ i) {
        for (var j = 0; j < this.nodes[i].length; ++ j) {
          var node = this.nodes[i][j];
          min_x = min(min_x, node.posX);
          min_y = min(min_y, node.posY);
          max_x = max(max_x, node.posX + node.node_width);
          max_y = max(max_y, node.posY + node.node_height);
        }
      }
      if (update_min_bounds) {
        this.svg_width = max_x - min_x + 1;
        this.svg_height = max_y - min_y + 1;
      }
      else {
        this.svg_width = max_x + 1;
        this.svg_height = max_y + 1;
      }
      if (this.svg_width < 100) this.svg_width = 100;
      if (this.svg_height < 100) this.svg_height = 100;
      this.svg.setAttribute('width', this.svg_width);
      this.svg.setAttribute('height', this.svg_height);
      for (var i = 0; i < this.nodes.length; ++ i) {
        for (var j = 0; j < this.nodes[i].length; ++ j) {
          var node = this.nodes[i][j];
          if (update_min_bounds) {
            node.posX -= min_x;
            node.posY -= min_y;
          }
          node.svg_node.setAttribute("transform", "translate(" + node.posX + ", " + node.posY +")");
          for (var k = 0; k < node.lines_out.length; ++ k) {
            var line = node.lines_out[k][0];
            var offset_y = node.lines_out[k][1];
            line.setAttribute("x1", node.posX + node.node_width);
            line.setAttribute("y1", node.posY + offset_y);
          }
          for (var k = 0; k < node.lines_in.length; ++ k) {
            var line = node.lines_in[k][0];
            var offset_y = node.lines_in[k][1];
            line.setAttribute("x2", node.posX);
            line.setAttribute("y2", node.posY + offset_y);
          }
        }
      }
      if (this.selected_pos != null) {
        if (update_min_bounds) {
          this.selected_pos[0] -= min_x;
          this.selected_pos[1] -= min_y;
        }
      }
    },

    mousemove(event) {
      if (! this.editable) return;
      var x = event.offsetX;
      var y = event.offsetY;
      if (this.selected_object != null && this.is_draging) { // nothing is being dragged
        var dx = x - this.selected_pos[0];
        var dy = y - this.selected_pos[1];
        this.mouse_moved = this.mouse_moved || (dx != 0 || dy != 0);
        this.selected_object.posX += dx;
        this.selected_object.posY += dy;
        this.selected_pos = [x, y];
        this._updateBounds(false);
        this._refresh_data_schema();
        return this._disabledEvent(event);
      }
      else if (this.context_menu != null) {
        if (x >= this.context_menu.x && y >= this.context_menu.y && 
          x <= this.context_menu.x + this.context_menu.node_width && 
          y <= this.context_menu.y + this.context_menu.node_height) {
          var item_height = this.font_size + this.text_margin;
          var y_offset = y - this.context_menu.y;
          for (var k = 0; k < this.context_menu.menu.length; ++ k) {
            if (y_offset >= this.text_margin + item_height * k && y_offset < this.text_margin + item_height * (k + 1)) {
              this.context_menu.rects[k].setAttribute("fill-opacity", 0.6);
            }
            else
              this.context_menu.rects[k].setAttribute("fill-opacity", 0);
          }
          return this._disabledEvent(event);
        }
      }
    },

    mouseup(event) {
      if (this.selected_object != null && this.is_draging) { // left cliked
        if (! this.mouse_moved) {
          this.selected_tablename = this.selected_object.table_name;
          if (this.event_listener != null) {
            this.event_listener('change', 'select');
            this.event_listener('change_select', null);
          }
        }
      }
      // this.selected_object = null;
      this.is_draging = false;
      this.mouse_moved = false;
      this._updateBounds(true);
      // return this._disabledEvent(event);
      return;
    },

    mouseleave(event) {
      // this.selected_object = null;
      this.is_draging = false;
      this.mouse_moved = false;
      this._updateBounds(true);
    },

    clearSvg() {
      $(this.svg).empty();
      this.context_menu = null;
    },

    draw() {
      this.clearSvg();
      if (this.nodes == null) return;

      var title_height = this.font_size + this.text_margin * 3;
      
      for (var i1 = 0; i1 < this.nodes.length; ++ i1) {
        for (var j1 = 0; j1 < this.nodes[i1].length; ++ j1) {
          var node1 = this.nodes[i1][j1];
          node1.lines_out = [];
          for (var i2 = 0; i2 < this.nodes.length; ++ i2) {
            for (var j2 = 0; j2 < this.nodes[i2].length; ++ j2) {
              var node2 = this.nodes[i2][j2];
              if (! ('lines_in' in node2)) node2.lines_in = [];
              for (var k1 = 0; k1 < node1.field_names.length; ++ k1) {
                if (! (node1.field_names[k1] in node1.foreign_keys)) continue;
                var foreign_key = node1.foreign_keys[node1.field_names[k1]];
                for (var k2 = 0; k2 < node2.field_names.length; ++ k2) {
                  if (foreign_key[0] == node2.table_name && foreign_key[1] == node2.field_names[k2]) {
                    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                    line.setAttribute("stroke", "#409EFF");
                    line.setAttribute("stroke-width", 3);
                    line.setAttribute("stroke-opacity", 0.6);
                    this.svg.appendChild(line);
                    node1.lines_out.push([line, title_height + (this.font_size + this.text_margin) * k1 + this.text_margin + this.font_size / 2]);
                    node2.lines_in.push([line, title_height + (this.font_size + this.text_margin) * k2 + this.text_margin + this.font_size / 2]);
                  }
                }
              }
            }
          }
        }
      }

      for (var i = 0; i < this.nodes.length; ++ i) {
        for (var j = 0; j < this.nodes[i].length; ++ j) {
          var node = this.nodes[i][j];
          node.rects = [];
          var svg_node = document.createElementNS("http://www.w3.org/2000/svg", "g");
          this.svg.appendChild(svg_node);
          node.svg_node = svg_node;
          // title background:
          var title_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          title_rect.setAttribute( "x", "0");
          title_rect.setAttribute( "y", "0");
          title_rect.setAttribute( "height", title_height);
          title_rect.setAttribute( "fill", "#409EFF");
          title_rect.setAttribute( "fill-opacity", 0.9);
          title_rect.setAttribute( "stroke", "#409EFF");
          title_rect.setAttribute("stroke-width", "1");
          svg_node.appendChild(title_rect);
          // title
          var title = document.createElementNS("http://www.w3.org/2000/svg", "text");
          var table_name = node.table_name;
          var table_type = '';
          if ('table_type' in node) table_type = node.table_type;
          if (table_type != '') table_name += ' (' + table_type + ')';
          title.textContent = table_name;
          title.setAttribute("font-size", this.font_size);
          title.setAttribute("font-weight", "bold");
          title.setAttribute("x", this.text_margin);
          title.setAttribute("y", this.font_size + this.text_margin);
          title.setAttribute("fill", "#FFFFFF");
          svg_node.appendChild(title);          
          // field rect
          var node_height = (this.font_size + this.text_margin) * (node.field_names.length + 1) + this.text_margin * 4 + 1
          var field_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          field_rect.setAttribute( "x", "0px");
          field_rect.setAttribute( "y", title_height);
          field_rect.setAttribute( "height", node_height - title_height);
          field_rect.setAttribute( "fill", "#FFFFFF");
          field_rect.setAttribute( "fill-opacity", 0.7);
          field_rect.setAttribute( "stroke", "#409EFF");
          field_rect.setAttribute("stroke-width", "1");
          svg_node.appendChild(field_rect);
          var max = function(x, y) {
            if (x == null) return y;
            if (y == null) return x;
            return x > y ? x : y;
          };
          var node_width = title.getBBox().width + 2 * this.text_margin;
          for (var k = 0; k < node.field_names.length; ++ k) {
            var text_y = title_height + (this.font_size + this.text_margin) * (k + 1);
            // text rect
            var text_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            text_rect.setAttribute("x", "0px");
            text_rect.setAttribute("y", (text_y - this.font_size + this.text_margin) + "px");
            text_rect.setAttribute("height", this.font_size);
            text_rect.setAttribute("fill", "#E6A23C");
            text_rect.setAttribute("fill-opacity", 0);
            text_rect.setAttribute("stroke-width", "0");
            svg_node.appendChild(text_rect);
               node.rects.push(text_rect);
            // field tpye
            var field_type = document.createElementNS("http://www.w3.org/2000/svg", "text");
            if (node.field_types[k] == 'number')
              field_type.textContent = 'N';
            else if (node.field_types[k] == 'text')
              field_type.textContent = 'T';
            else if (node.field_types[k] == 'time')
              field_type.textContent = 'D';
            else if (node.field_types[k] == 'boolean')
              field_type.textContent = 'B';
            else {
              console.log('Unknown return type: ' + node.field_types[k])
              field_type.textContent = '?';
            }
            field_type.setAttribute("font-size", this.font_size);
            field_type.setAttribute("x", 1 + this.text_margin);
            field_type.setAttribute("y", text_y);
            field_type.setAttribute("fill", "#A4A4A4");
            svg_node.appendChild(field_type);          
            // field name
            var field_name = document.createElementNS("http://www.w3.org/2000/svg", "text");
            field_name.textContent = node.field_names[k];
            field_name.setAttribute("font-size", this.font_size);
            field_name.setAttribute("x", 1 + this.text_margin + this.font_size);
            field_name.setAttribute("y", text_y);
            if (node.primary_keys.indexOf(node.field_names[k]) != -1)
              field_name.setAttribute("fill", "#F56C6C");
            else if (node.field_names[k] in node.foreign_keys)
              field_name.setAttribute("fill", "#409EFF");
            else
              field_name.setAttribute("fill", "#000000");
            svg_node.appendChild(field_name);
            node_width = max(node_width, field_name.getBBox().width + 2 * this.text_margin + this.font_size + 2);
          }
          title_rect.setAttribute("width", node_width);
          field_rect.setAttribute("width", node_width);
          for (var k = 0; k < node.rects.length; ++ k)
              node.rects[k].setAttribute("width", node_width);
          node.node_width = node_width;
          node.node_height = node_height;
        }
      }

      if (this.nodes.length > 0 && this.nodes[0].length > 0 && ! ('posX' in this.nodes[0][0])) {
        var current_x = 0;
        for (var i = 0; i < this.nodes.length; ++ i) {
          var level_x = 0;
          for (var j = 0; j < this.nodes[i].length; ++ j) {
            level_x = max(level_x, this.nodes[i][j].node_width);
          }
          for (var j = 0; j < this.nodes[i].length; ++ j) {
            this.nodes[i][j].posX = current_x;
          }
          current_x += level_x + this.node_margin * 2;
        }
        // this.svg_width = current_x - this.node_margin * 2;
        // this.svg_height = 0;
        for (var i = this.nodes.length - 1; i >= 0; -- i) {
          var current_y = 0;
          for (var j = 0; j < this.nodes[i].length; ++ j) {
            this.nodes[i][j].posY = current_y;
            current_y += this.nodes[i][j].node_height + this.node_margin;
          }
          // this.svg_height = max(this.svg_height, current_y - this.node_margin);
        }
      }
      this._updateBounds(true);
    },

    _set_data(data_, emit_event=false) {
      this.clearSvg();
      this.nodes = [];
      if (data_ == null || data_.length == 0) return;
      this.nodes = [];
      for (let table_name in data_) {
        if (table_name == '__update_time__') continue;
        data_[table_name].table_name = table_name
        if (! ('table_type' in data_[table_name]))
          data_[table_name].table_type = ''
        this.nodes.push(data_[table_name]);
      }
      this._init_node_pos();
      this.draw();
      this._refresh_data_schema();
      if (emit_event) 
        if (this.event_listener != null) {
          this.event_listener('change', 'data');
          this.event_listener('change_data', null);
        }
    },

    _refresh_data_schema() {
      // var rows = {};
      // for (var k = 0; k < this.data[0].value.length; ++ k)
      //     rows[this.data[0].value[k].table_name] = this.data[0].value[k].rows;
      old_data = this.data
      this.data = {};
      this.data['__update_time__'] = old_data['__update_time__'];
      for (var i = 0; i < this.nodes.length; ++ i) {
        for (var j = 0; j < this.nodes[i].length; ++ j) {
          var node = this.nodes[i][j];
          var node2 = {};
          node2.table_name = node.table_name;
          node2.table_type = node.table_type;
          node2.posX = node.posX;
          node2.posY = node.posY;
          node2.field_names = node.field_names;
          node2.field_types = node.field_types;
          node2.foreign_keys = node.foreign_keys;
          node2.primary_keys = node.primary_keys;
          // node2.rows = rows[node.table_name];
          this.data[node2.table_name] = node2
        }
      }      
    },

    _init_node_pos() {
      if (this.nodes.length == 0) return;
      // node order
      var child_index = function(p, c) {
        for (var i = 0; i < p.field_names.length; ++ i) {
          if (p.field_names[i] in p.foreign_keys) {
            var c_name = p.foreign_keys[p.field_names[i]][0];
            if (c.table_name == c_name) return i;
          }
        }
        return -1;
      }
      var child_count = function(p) {
        var count = 0;
        for (var i = 0; i < p.field_names.length; ++ i) {
          if (p.field_names[i] in p.foreign_keys) ++ count;
        }
        return count;
      }
      var relative_pos = function(node1, node2) {
        var ci1 = child_index(node1, node2);
        if (ci1 != -1) {
          var cc1 = child_count(node1);
          return (cc1 - 1) / 2 - ci1;
        }
        var ci2 = child_index(node2, node1);
        if (ci2 != -1) {
          var cc2 = child_count(node2);
          return ci2 - (cc2 - 1) / 2;
        }
        return 0;
      }     
      var topological_sort = function(nodes, is_parent) {
        var levels = [];
        var no_level = [];
        for (var i = 0; i < nodes.length; ++ i) {
          no_level.push(nodes[i]);
        }
        for (var l = 0; l < nodes.length; ++ l) {
          var nodes_have_parent = [];
          for (var i = 0; i < no_level.length; ++ i) {
            var has_parent = false;
            for (var j = 0; j < no_level.length; ++ j) {
              if (i == j) continue;
              if (is_parent(no_level[j], no_level[i])) {
                has_parent = true;
                break;
              }
            }
            if (has_parent) {
              nodes_have_parent.push(no_level[i]);
            }
          }
          var nodes_have_no_parent = [];
          for (var i = 0; i < no_level.length; ++ i) {
            if (nodes_have_parent.indexOf(no_level[i]) == -1) {
              nodes_have_no_parent.push(no_level[i]);
            }
          }
          if (nodes_have_no_parent.length == 0) {
            levels.push(nodes_have_parent);
            break;
          }
          levels.push(nodes_have_no_parent);
          if (nodes_have_parent.length == 0) {
            break;
          }
          no_level = nodes_have_parent;
        }
        return levels;
      }
      var y_levels = topological_sort(this.nodes, (node1, node2) => {
        return relative_pos(node1, node2) < 0;
      });
      var count = 0;
      for (var i = 0; i < y_levels.length; ++ i) {
        for (var j = 0; j < y_levels[i].length; ++ j) {
          y_levels[i][j].count = count ++;
        }
      }
      y_levels = null;
      var x_levels = topological_sort(this.nodes, (node1, node2) => {
        return child_index(node1, node2) != -1;
      });
      var sort = function(nodes, cmp) {
        for (var j = nodes.length - 1; j > 0; --j) {
          for (var i = 0; i < j;  ++ i) {
            if (cmp(nodes[i], nodes[i + 1]) > 0) {
              var tmp = nodes[i];
              nodes[i] = nodes[i + 1];
              nodes[i + 1] = tmp;
            }
          }
        }
      }
      for (var i = 0; i < x_levels.length; ++ i) {
        sort(x_levels[i], (node1, node2) => { return node1.count - node2.count; })
      }
      this.nodes = x_levels;
    }      

  }

  obj.elt = document.createElement("div");
  obj.elt.setAttribute("style", "padding:8px")
  // obj.elt.setAttribute("focusable", "true");
  return obj;
}
