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


function page_config_editor_obj_js() {
  var obj = {
    type_name: 'page_config_editor',
    elt: null,
    event_listener: null,
    component: null,

    use_example_data() {
      $('<div class="alert alert-info" role="alert">'+this.type_name+'</div>').appendTo($(this.elt));
    },
    get_var(var_name) {
      if (this.component == null) return null;
      return JSON.stringify(this.component);
    },
    set_var(var_name, var_) {
      this.component = null;
      $(obj.elt).empty();
      if (var_ == null) return;
      this.component = JSON.parse(var_)
      // built table element
      var tb = $('<table></table>', {'class':'small table table-sm table-hover '}).appendTo($(obj.elt));
      var thead = $('<thead></thead>', {'class':'thead-dark'}).appendTo(tb);
      var tbody = $('<tbody></tbody>').appendTo(tb);
      var tr = $('<tr></tr>').appendTo(thead);
      $('<th></th>').appendTo(tr);
      $('<th>页面参数</th>').appendTo(tr);
      $('<th>设置值</th>').appendTo(tr);
      tr = $('<tr></tr>', {'class':'table-info'}).appendTo(tbody);
      $('<td><span class="badge badge-info">page</span></td>').appendTo(tr);
      $('<td>何时显示</td>').appendTo(tr);
      var dropdown = $('<td></td>', {'class':'dropdown'}).appendTo(tr);
      var a = $('<a></a>', {'text':this.component[1], 'class':'dropdown-toggle', 'data-toggle':'dropdown', 
                  'aria-haspopup':'true', 'aria-expanded':'false', 'id':'page_config_editor_select_id_1'}).appendTo(dropdown);
      var ll = $('<div></div>', {'class':'dropdown-menu', 'aria-labelledby':'page_config_editor_select_id_1'}).appendTo(dropdown);
      choices = ['', 'login', 'logout', 'owner'].forEach(tt => {
        var li = $('<a></a>', {'text':tt, 'class':'dropdown-item small'}).appendTo(ll);
        li.bind('click', ev => {
          a.text(ev.target.text);
          if (this.component[1] != ev.target.text) {
            this.component[1] = ev.target.text;
            this.event_listener('change', 'component');
          }
        });
      });
      tr = $('<tr></tr>', {'class':'table-info'}).appendTo(tbody);
      $('<td></td>').appendTo(tr);
      $('<td></td>').appendTo(tr);
      var td = $('<td></td>').appendTo(tr);
      var del_btn = $('<button type=button class="btn-sm btn-dark" style="font-size:smaller;">删除页面 "'+this.component[0]+'"</button>').appendTo(td);
      del_btn.bind('click', () => {
        confirm_modal('请确认删除页面: ' + this.component[0], () => {
          this.set_var(null, null);
          this.event_listener('change', 'component');
        });
      });
    }

  };
  obj.elt = document.createElement("div");
  // obj.elt.setAttribute("style", "padding:8px")
  return obj;
}

