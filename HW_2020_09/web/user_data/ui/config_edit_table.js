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

var config_edit_table_select_id = 0;

function _config_edit_table_fix_meta(meta) {
  if (! ('ref' in meta)) {
    meta['ref'] = []
  }
  if ('vars' in meta) {
    for (var i in meta['vars']) {
      var v = meta['vars'][i];
      if (meta['data'].indexOf(v) == -1)
        meta['data'].push(v);
    }
    delete meta['vars'];
  }
}

function _editing_lines(config, meta, table_names, event_names, var_names) {
  var lines = [];
  lines.push([null, '名字', meta.name, []]);
  if ('tag' in config && config.tag[0] != '#' && config.tag[0] != '$') {
    lines.push([null, 'text', config.text, null]);
  }
  ['data', 'ref', 'event' ].forEach(tt => {
      var tts = (tt != 'event' ? tt : tt + 's');
      meta[tts].forEach(d => {
        var choices = [' ']
        if (tt == 'data') choices = choices.concat(table_names, event_names, var_names);
        if (tt == 'ref') choices = choices.concat(table_names, event_names, var_names);
        if (tt == 'event') choices = choices.concat(event_names,['@同步']);
        lines.push([tt, d, (d in config[tts] ? config[tts][d] : ''), choices]); // '' -> tabe_name | var_name | event_name
      }); 
  });
  for (var d in meta['class']) {
    var choices = meta['class'][d]
    if (choices.length == 1) continue;
    var c = '';
    if ('class' in config) {
      var cs = config['class'].split(/[ ]+/);
      cs.forEach(c1 => {
        if (choices.indexOf(c1) != -1) c = c1;
      });
    }
    lines.push(['class', d, c, choices]);
  }
  ['style', 'attr'].forEach(tt => {
      for (var d in meta[tt]) {
        var choices = meta[tt][d]
        if (choices.length == 1) continue;
        var c = '';
        if (d in config[tt]) c = config[tt][d];
        lines.push([tt, d, c, choices]);
      };
  });
  return lines;
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

function _new_config(lines, meta) {
  // var name_regex = /^[a-zA-Z_$][a-zA-Z_0-9]*(\:[a-zA-Z$][a-zA-Z_0-9]*)?$/
  var config = {'__meta__':meta};
  if ('tag' in meta && meta.tag != '') config.tag = meta.tag;
  if ('init' in meta && meta.init != '') {
    config.init = meta.init;
    if ('files' in meta) {
      config.files = meta.files;
    }
  }
  var clazz = [];
  if ('class' in meta)
    for (var d in meta['class'])
      if (meta['class'][d].length == 1 && meta['class'][d][0].trim() != '')
        clazz.push(meta['class'][d][0].trim());
  config.data = {};
  config.ref = {};
  config.events = {};
  config.style = {};
  config.attr = {};
  ['style', 'attr'].forEach(tt => {
      for (var d in meta[tt])
        if (meta[tt][d].length == 1)
          config[tt][d] = meta[tt][d][0];
  });
  var error = null;
  lines.forEach(line => {
    var tt = line[0];
    var name = line[1];
    var value = line[2].trim();
    if (tt == null) {
      if (name == 'text') {
        if (value == '') error = '"text" 不能为空';
        else config.text = value;
      }
    } 
    else if (tt == 'data' || tt == 'ref' || tt == 'event') {
      var tts = (tt != 'event' ? tt : tt + 's');
      if (value != '') {
        var value1 = value
        if (tt == 'data' || tt == 'ref') {
          if (value[0] == '$')
            value1 = value.substring(1);
        }
        if (error != null) {
          if (! is_identifier(value1)) error = '"'+tt+'" 格式错误';
        }
      }
      if (error == null && value != '') config[tts][name] = value;
    }
    else if (tt == 'class') {
      if (value != '') clazz.push(value);
    }
    else if (tt == 'attr' || tt == 'style') {
      if (value != '') config[tt][name] = value;
    }
  });
  if (clazz.length > 0) {
    config['class'] = ''
    clazz.forEach(c => {config['class'] += c + ' '});
    config['class'] = config['class'].trim();
  }
  if (error != null) {
    error_toast(error);
    return null;
  }
  return config;
}

function _populate_tbody(tbody, lines, on_change) {
  function create_tr(tt, name, tr_class) {
    var tr = $('<tr></tr>', {'class':'table-'+tr_class}).appendTo(tbody); 
    if (tt == null) $('<td></td>').appendTo(tr);
    else $('<td style="text-align:right;"><span class="badge badge-'+tr_class+'">'+tt+'</span></td>').appendTo(tr);
    $('<td><a>'+name+'</a></td>').appendTo(tr);
    return tr;
  }
  function create_constant(tt, name, value, tr_class) {
    var tr = create_tr(tt, name, tr_class);
    var td = $('<td></td>').appendTo(tr);
    $('<a></a>', {'text':value}).appendTo(td);
  }
  function create_input(tt, name, value, line, tr_class) {
    var tr = create_tr(tt, name, tr_class);
    var td = $('<td></td>').appendTo(tr);
    var input = $('<a></a>', {'text':value, 'contenteditable':true}).appendTo(td);
    input.bind('blur', ev => {
      line[2] = input.text();
      on_change()
    });
  }
  function create_select(tt, name, value, choices, line, tr_class) {
    var tr = create_tr(tt, name, tr_class);
    var dropdown = $('<td></td>', {'class':'dropdown'}).appendTo(tr);
    var a = $('<a></a>', {'text':value, 'class':'dropdown-toggle', 'data-toggle':'dropdown', 
                  'aria-haspopup':'true', 'aria-expanded':'false', 'id':'config_edit_table_select_id_' + config_edit_table_select_id}).appendTo(dropdown);
    var ll = $('<div></div>', {'class':'dropdown-menu', 'aria-labelledby':'config_edit_table_select_id_' + config_edit_table_select_id}).appendTo(dropdown);
    config_edit_table_select_id += 1;
    choices.forEach(tt => {
      var li = $('<a></a>', {'text':tt, 'class':'dropdown-item small'}).appendTo(ll);
      li.bind('click', ev => {
        a.text(ev.target.text);
        line[2] = ev.target.text;
        on_change();
      });
    });
  }
  lines.forEach(line => {
    var tt = line[0];
    var name = line[1];
    var value = line[2];
    var choices = line[3];
    if (tt == null) {
        if (name == '名字') create_constant(null, '控件名', value, 'secondary');
        else create_input(null, name, value, line, 'primary');
    }
    else if (choices == null) create_input(tt, name, value, line, 'success');
    else if (choices.length > 0) {
      var color = 'danger';
      if (tt == 'data' || tt == 'ref' || tt == 'event') color = 'success';
      create_select(tt, name, value, choices, line, color);
    }
    else create_input(tt, name, value, line, 'danger');
  });    
}

function _create_table(parent, lines, on_change) {
  var tb = $('<table></table>', {'class':'small table table-sm table-hover '}).appendTo(parent);
  var thead = $('<thead></thead>', {'class':'thead-dark'}).appendTo(tb);
  var tbody = $('<tbody></tbody>').appendTo(tb);
  var tr = $('<tr></tr>').appendTo(thead);
  ['','控件参数', '设置值'].forEach(name => $('<th>' + name + '</th>').appendTo(tr));
  _populate_tbody(tbody, lines, on_change);
}

function _config_changed(config1, config2) {
  if (config1 == null || config2 == null) return false;
  config1 = JSON.stringify(config1);
  config2 = JSON.stringify(config2);
  return config1 != config2;
}

function config_edit_table_obj_js() {
  var obj = {
    type_name: 'config_edit_table',
    elt: null,
    event_listener: null,
    config: null,
    page: null,
    table_names: [],
    table_names_data: null,
    event_names: [],
    var_names: [],

    use_example_data() {
    	$('<div class="alert alert-info" role="alert">'+obj.type_name+'</div>').appendTo($(this.elt));
    },
    get_data_json_text(data_name) {
      if (data_name == 'config') {
        if (this.config == null) return null;
        return JSON.stringify(this.config);
      }
      return null;
    },
    _update_names() {
      this.table_names = [];
      this.event_names = [];
      this.var_names = ['$变量1', '$变量2', '$变量3', '$变量4', '$变量5', '$变量6', '$变量7', '$变量8', '$变量9'];
      var login = 'logout'; // 'logout', 'login', 'owner'
      if (this.page != null) {
        var at = this.page['rows'][0][1];
        if (at.startsWith('登录后') || at.startsWith('用户组')) login = 'login';
        if (at.startsWith('网站作者')) login = 'owner';
        if (at.startsWith('测试')) {
          login = 'test';
          this.var_names = [];
        }
      }
      data = this.table_names_data;
      if (data == null) return;
      user_id = JSON.parse(window.user_info)['user']
      for (var i = 0; i < data['rows'].length; ++ i) {
        var name =  data['rows'][i][0];
        var access_type =  data['rows'][i][1]; // '', 'public', 'client', 'big'
        if (name[0] == '@') {
          if (login != 'test' && name.startsWith('@'+user_id+'_'))
            this.event_names.push(name); // actions are responsible for their own access control
        }
        else {
          if (access_type != 'public') {
            if (login == 'logout') continue; // non-public data requires login
            if (login == 'login' && access_type != 'client') continue; // non-owner cannot access data other than pubilc and client
          }
          this.table_names.push(name);
        }
      }
      // console.log('this.table_names', this.table_names);
      // console.log('this.event_names', this.event_names);
    },
    set_data(data_name, data) {
      if (data_name == 'config') {
        this.config = null;
        $(obj.elt).empty();
        if (data == null) return;
        this.config = data
        var meta = this.config.__meta__
        _config_edit_table_fix_meta(meta);
        var lines = _editing_lines(this.config, meta, this.table_names, this.event_names, this.var_names);
        var this_ = this;
        _create_table($(obj.elt), lines, () => {
          var new_config = _new_config(lines, meta);
          if (_config_changed(this_.config, new_config)) {
            this_.config = new_config;
            this_.event_listener('change', 'config')
          }
        });
      }
      else if (data_name == 'page') {
        this.page = data;
        this._update_names();
      }
      else if (data_name == 'data') {
        this.table_names_data = data;
        this._update_names();
        this.set_data('config', this.config);
      }
      else {
        error_toast('No such data: ' + data_name);
      }
    }

  };
  obj.elt = document.createElement("div");
  return obj;
}

