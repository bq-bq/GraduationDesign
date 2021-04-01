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

function _component_edit_table_fix_config_template(config_template) {
  if ('vars' in config_template) {
    for (var i in config_template['vars']) {
      config_template['data'].push(config_template['vars'][i]);
    }
    delete config_template['vars'];
  }
  if (! ('ref' in config_template))
    config_template['ref'] = [];
}

function component_edit_table_obj_js() {
  var obj = {
    type_name: 'component_edit_table',
    elt: null,
    event_listener: null,
    editing: null,

    use_example_data() {
      $('<div class="alert alert-info" role="alert">'+obj.type_name+'</div>').appendTo($(this.elt));
    },
    get_data_json_text(data_name) {
      if (this.editing == null) return null;
      text = JSON.stringify(this.editing);
      return text
    },
    set_data(data_name, data) {
      var this_ = this;
      this.editing = null;
      $(obj.elt).empty();
      if (data == null) return;
      this.editing = data
      var component_id = this.editing['rows'][0][0];
      var config_template1 = this.editing['rows'][0][1]
      var from = null;
      if (config_template1 == '') {
        config_template = {name:component_id, tag:'', text:'', init:'', files:[], data:[], ref:[], events:[], class:{}, attr:{}, style:{}}
      }
      else {
        config_template = JSON.parse(config_template1);
        _component_edit_table_fix_config_template(config_template);
        if ('from' in config_template) {
          from = config_template['from']; // if the component is from the element store, from is the publisher of the component
          delete config_template['from'];
        }
      }
      var tb = $('<table></table>', {'class':'small table table-sm table-hover table-responsive'}).appendTo($(obj.elt));
      var thead = $('<thead></thead>', {'class':'thead-dark'}).appendTo(tb);
      var tbody = $('<tbody></tbody>').appendTo(tb);
      var tr = $('<tr></tr>').appendTo(thead);
      var headers = ['参数', '名字', '值'];
      headers.forEach(name => $('<th>' + name + '</th>').appendTo(tr));
      function onblur(ev) {
        var lines = [];
        tbody.children('tr').each(function(i) {
          tr = $(this)[0];
          var line = [];
          for (var i = 0; i < tr.childNodes.length; ++ i) {
            line.push(tr.childNodes[i].childNodes[0].text.trim());
          };
          if (! (line[0] == '' && line[1] == '' && (line[2] == '' || line[2] == 'N/A'))) lines.push(line);
        });
        // read from table
        var config_template2 = {name:component_id, tag:'', text:'', init:'', files:[], data:[], ref:[], events:[], class:{}, attr:{}, style:{}}
        lines.forEach(line => {
          var key = line[0].trim();
          var name = line[1].trim();
          var value = line[2].trim();
          switch (key) {
            case '控件名': break;
            case 'tag':
            case 'text':
            case 'init':
              config_template2[key] = name;
              break;
            case 'import':
            case 'data':
            case 'ref':
            case 'event':
              if (key == 'import') key = 'files';
              if (key == 'event') key = 'events';
              if (name != '') {
                config_template2[key].push(name);
              }
              break;
            case 'class':
            case 'attr':
            case 'style':
              if (name in config_template2[key]) {
                if (value != '')
                  config_template2[key][name] = config_template2[key][name].concat(value.split(','));
              }
              else {
                if (name != '')
                  if (value == '')
                    config_template2[key][name] = [];
                  else
                    config_template2[key][name] = value.split(',');
              }
              break;
            default:
              if (! (key == '' && (name == '+' || name == '') && value == ''))
                config_template2[key] = [name, value];
          }
        });
        // console.log(config_template2);
        // check correctness
        if ('' in config_template2) {
          error_toast('缺少参数');
          return;
        }
        if (config_template2['tag'] == '' && config_template2['init'] == '') {
          error_toast('"tag" 或 "init" 其中一个不能为空');
          return;
        }
        if (config_template2['tag'] != '' && config_template2['init'] != '') {
          error_toast('"tag" 或 "init" 其中一个需要为空');
          return;
        }
        for (var name in config_template2['class']) {
          if (config_template2['class'][name].length == 0) {
            error_toast('class 集合 "' + name + '" 中不能没有成员');
            return;
          }
        }
        for (var i in config_template2['files']) {
          var file = config_template2['files'][i];
          if (! (file.endsWith('.js') || file.endsWith('.css') || file.endsWith('.py'))) {
            error_toast('文件 "'+ file +'" 只能以 .py 或 .js 或 .css 结尾');
            return;
          }
        }
        if (config_template2['tag'] != '' && (config_template2['tag'][0] != '#' && config_template2['tag'][0] != '$')) {
          if (config_template2['data'].length != 0) {
            error_toast('使用 tag 定义的控件不能定义 data');
            return;
          }
        }

        // update data
        if (from != null) config_template2['from'] = from;
        config_template3 = JSON.stringify(config_template2);
        if (config_template1 == config_template3) return;
        config_template1 = config_template3;
        this_.editing['rows'][0][1] = config_template3;
        this_.set_data(null, this_.editing);
        if (this_.event_listener != null)
          this_.event_listener('change', 'editing');
      }
      // set var
      function add_row(row, editable) {
        tr = $('<tr></tr>').appendTo(tbody);
        row.forEach(name => {
          var td = $('<td></td>').appendTo(tr)
          var a = $('<a' + ((editable&&name!=null)?'':' class="text-secondary"') + 
                    ' contenteditable=' + ((editable&&name!=null)?'true':'false') + '>' + 
                    (name!=null?name:'N/A') + '</a>').appendTo(td);
          a.bind('blur', onblur);
        });
        return tr;
      }
      add_row(['控件名', component_id, null], false).addClass('table-secondary');
      add_row(['tag', config_template['tag'], null], true).addClass('table-primary');
      add_row(['text', config_template['text'], null], true).addClass('table-primary');
      add_row(['init', config_template['init'], null], true).addClass('table-primary');
      var has_import = false;
      config_template['files'].forEach(file => {
        add_row(['import', file, null], true).addClass('table-info');
        has_import = true;
      });
      if (! has_import) add_row(['import', '', null], true).addClass('table-info');
      var dd = {'data':'data', 'ref':'ref', 'events':'event'};
      Object.keys(dd).sort().forEach(d => {
        config_template[d].sort().forEach(name => {
          add_row([dd[d], name, null], true).addClass('table-success');
        });
        if (Object.keys(config_template[d]).length == 0)
          add_row([dd[d], '', null], true).addClass('table-success');
      });
      dd = ['class', 'attr', 'style'];
      dd.forEach(d => {
        Object.keys(config_template[d]).sort().forEach(name => {
          var val = ''
          for (var i = 0; i < config_template[d][name].length; ++ i) {
            if (i > 0) val += ',';
            val += config_template[d][name][i].trim();
          }
          add_row([d, name, val], true).addClass('table-danger');
        });
        if (Object.keys(config_template[d]).length == 0)
          add_row([d, '', ''], true).addClass('table-danger');
      });
      dd = ['name', 'tag', 'text', 'init', 'files', 'data', 'ref', 'events', 'class', 'attr', 'style']
      var some_error = false;
      Object.keys(config_template).sort().forEach(type_ => {
        if (dd.indexOf(type_) == -1) {
          d = config_template[type_];
          if (! (type_ == '' && d[0] == '' && d[1] == '')) {
            add_row([type_, d[0], d[1]], true).addClass('text-primary'); 
            some_error = true;
          }
        }
      });
      if (! some_error) {
        add_row(['', '+', ''], true).addClass('text-primary');
      }
      var del_btn = $('<button type="button" class="btn btn-danger">删除控件 "' + component_id + '"</button>').appendTo($(obj.elt));
      del_btn.bind('click', ev => {
        confirm_modal('请确认删控件 "' + component_id + '"', ()=> {
          this_.set_data(null, null)
          if (this_.event_listener != null)
            this_.event_listener('change', 'editing');
        });
      })
    }
  };
  obj.elt = document.createElement("div");
  obj.elt.setAttribute("style", "padding:8px")
  // $('<div class="alert alert-info" role="alert">'+obj.type_name+'</div>').appendTo($(obj.elt));
  return obj;
}

