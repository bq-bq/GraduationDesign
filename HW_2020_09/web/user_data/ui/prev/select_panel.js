/*
elt
mounted(config)
dispose()
event_listener
set_data(data_name, data)
get_data_json_text(data_name)
set_var(var_name, var_)
get_var(var_name)
*/

function select_panel_obj_js() {
  var obj = {
    type_name: 'select_panel',
    data: null,
    elt: null,
    event_listener: null,
    selected_row: null,
    expandable: 'true',
    item_name: '项',
    width: '130px',
    key_column: 0,
    val_column: -1,

    use_example_data() {
      this.data = {'field_names':['item_name','item_data'], 'field_types':['text','text'], 'rows':[['选项1',''],['选项2','']]};
    },
    mounted(config, is_editing, edit_listener) {
      if ('attr' in config) {
        if ('item_name' in config.attr)
          this.item_name = config.attr.item_name;
        if ('width' in config.attr)
          this.width = config.attr.width;
        if ('expandable' in config.attr)
          this.expandable = config.attr.expandable;
        if ('data_columns' in config.attr) {
          data_columns = config.attr.data_columns.split(',');
          if (data_columns.length == 1) {
            this.key_column = parseInt(data_columns[0]) - 1;
            this.val_column = -1;
          }
          else {
            this.key_column = parseInt(data_columns[0]) - 1;
            this.val_column = parseInt(data_columns[1]) - 1;
          }
        }
      }
      this.set_data(null, this.data, false);
    },
    set_var(var_name, var_) {
      var index = this.data.rows.indexOf(this.selected_row);
      if (var_ == null) {
        var item_name = this.data.rows[index][this.key_column];
        this.data.rows.splice(index, 1);      
        this.set_data(null, this.data, false);
        info_toast('已删除'+this.item_name+': ' + item_name);
      }
      else {
        if (this.val_column != -1) {
          this.selected_row[this.val_column] = var_;
        }
        else {
          var row1 = JSON.parse(var_)
          var row2 = this.selected_row;
          for (var i = 0; i < row1.length; ++ i) row2[i] = row1[i];
        }
        info_toast('已保存'+this.item_name+': ' + this.selected_row[this.key_column]);
      }
      if (this.event_listener != null) {
        this.event_listener('change', 'data');
        this.event_listener('data_change', 'data');
      }
    },
    get_var(var_name) {
      if (this.selected_row == null) return null;
      if (this.val_column != -1) {	
        return this.selected_row[this.val_column];
      }
      else {
        return JSON.stringify(this.selected_row);
      }
    },
    get_data_json_text(data_name) {
      return JSON.stringify(this.data);
    },

    set_data(data_name, data_, edited=true) {
      $(this.elt).empty().css('width', this.width)
      this.data = null;
      this.selected_row = null;
      if (edited && this.event_listener != null)
        this.event_listener('change', 'selected');
      if (data_ == null || ! ('rows' in data_)) return;
      this.data = data_;
      var list_group = $('<ul/>', { 'class':'list-group' }).appendTo($(this.elt));
      var this_ = this;
      function input_new_component_name(action) {
        var image = 'web/lib/icons/bootstrap/document-text.svg'
        var inputs=[{'type':'text', 'id':'input_text', 'placeholder':''}];
        function callback(d) {
          d = d[0].trim();
          if (d == '') {
            error_toast('没有输入');
            return;
          }
          action(d);
        }
        data_modal(image, '请输入新'+this_.item_name+'的名字', inputs, 'OK', callback);
      }
      var selected_item = null;
      function select_item(item) {
        if (item != null) {
          item.removeClass('list-group-item-primary');
          item.addClass('list-group-item-danger');
        }
        if (selected_item != null) {
          selected_item.removeClass('list-group-item-danger');
          selected_item.addClass('list-group-item-primary');
        }
        selected_item = item;
      }
      function add_row(row) {
        var item = $('<li/>', { 'class':'list-group-item list-group-item-primary', 
                      append:row[this_.key_column],
                      on: {
                        click: () => {
                          select_item(item);
                          this_.selected_row = row;
                          if (this_.event_listener != null)
                            this_.event_listener('change', 'selected');
                        }
                      }
                    }).appendTo(list_group);
      }
      this.data.rows.forEach(add_row);
      if (this.expandable == 'false') return;
      var add_item = $('<li/>', { 'class':'list-group-item list-group-item-secondary',
                    append:'+ 添加'+this.item_name,
                    on: {
                      click: () => {
                        input_new_component_name(name => {
                          // reset selected
                          select_item(null);
                          this_.selected_row = null;
                          if (this_.event_listener != null)
                            this_.event_listener('change', 'selected');
                          // var config_template = {name:name, tag:'', text:'', init:'', files:[], data:[], vars:[], events:[], class:{}, attr:{}, style:{}}
                          var row = [  ]
                          for (var i = 0; i < this_.data.field_names.length; ++ i)
                            row.push('');
                          row[this_.key_column] = name;
                          this_.data.rows.push(row);
                          this_.set_data(null, this_.data, false);
                          if (this_.event_listener != null) {
                            this_.event_listener('change', 'data');
                            this_.event_listener('data_change', 'data');
                          }
                          info_toast('已保存'+this_.item_name+': ' + name);
                        });
                      }
                    }
                  }).appendTo(list_group);
    }
  };
  obj.elt = document.createElement("div");
  $(obj.elt).addClass('smooth-scroll').attr('overflow', 'auto');
  return obj;
}

