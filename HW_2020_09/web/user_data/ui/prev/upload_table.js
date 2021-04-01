/*
elt
mounted(config)
dispose()
event_listener
set_data(data_name, data)
get_data(data_name)
set_var(var_name, var_)
get_var(var_name)
*/

function upload_table_obj_js() {
  var obj = {
    type_name: 'upload_table',
    data: {},
    elt: null,
    event_listener: null,

    use_example_data() {
      $('<div class="alert alert-info" role="alert">'+this.type_name+'</div>').appendTo($(this.elt));
    },
    // mounted(config) {
    //   this.set_data(null, this.data);
    // },
    dispose() {
    },
    set_data(data_name, data_) {
      $(this.elt).empty();
      this.elt.setAttribute('style', 'margin:10px;');
      this.data = null;
      if (data_ == null || ! ('field_names' in data_))return;
      this.data = data_;
      var tb = document.createElement("table");
      tb.setAttribute("class", "small table table-sm table-striped table-hover table-bordered table-responsive");
      this.elt.appendChild(tb);
      var thead = document.createElement("thead");
      thead.setAttribute("class", "thead-dark");
      tb.appendChild(thead);
      var tbody = document.createElement("tbody");
      tb.appendChild(tbody);
      var tr = document.createElement("tr");
      thead.appendChild(tr);
      var th = document.createElement("th");
      tr.appendChild(th);
      ['文件路径', '操作'].forEach(field_name => {
        th = document.createElement("th");
        tr.appendChild(th);
        var a = document.createElement("a");
        th.appendChild(a);
        a.text = field_name;
      });
      var this_ = this;
      function add_text_cell(tr, text, gray_text) {
        var td = document.createElement("td");
        tr.appendChild(td);
        var a = document.createElement("a");
        td.appendChild(a);
        if (gray_text)
          a.setAttribute("class", "text-secondary");
        a.text = text;
      }
      function add_button_cell(tr, id, text, event, callback) {
        var td = document.createElement("td");
        tr.appendChild(td);
        var a = document.createElement("button");
        td.appendChild(a);
        a.setAttribute("type", 'button');
        a.setAttribute("class", "btn btn-primary btn-sm");
        a.id = id;
        a.innerHTML = text;
        $(a).bind(event, callback);
      }
      function upload_file(files) {
        if (files.length == 0) return;
        if (files.length >= 20) {
          window.error_toast('一次不能上传超过20个文件');
          return;
        }
        var form_data = new FormData();
        form_data.append('user_info', user_info);
        // if (! file.type.match('image.*')) { error_toast('only image is allowed'); return; }
        for (var i = 0; i < files.length; ++ i) {
          if (files[i].size >= 100000000 ) { error_toast('文件大小限制: 100MB'); return; }
          form_data.append('file' + (i+1), files[i]);
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.onload = function () {
          if (xhr.status === 200) {
            var reply = JSON.parse(xhr.responseText);
            if ('url' in reply) {
              if (this_.event_listener != null)
                this_.event_listener('add', reply['url'])
              info_toast('已上传' + files.length + '个文件');
              return;
            }
            if ('error' in reply) {
              error_toast('上传失败: ' + reply['error']);
            }
          }
          else {
            error_toast('上传失败');
          }
        }
        xhr.send(form_data);
      }
      function add_file_cell(tr) {
        var td = document.createElement("td");
        tr.appendChild(td);
        var button = document.createElement("button");
        td.appendChild(button)
        button.id = 'upload-table-submit'
        button.innerHTML = '+'
        button.setAttribute("type", 'button');
        button.setAttribute("class", 'btn btn-success btn-sm');

        var file = $('<input type="file" style="display:none">');
        file.attr('multiple', 'multiple');
        file.attr('name', 'file[]');
        file.on('change', function(){
          upload_file(this.files);
        });
        $(button).after(file);
        $(button).bind('click', ev => file.click());
      }
      function delete_file(ev) {
        confirm_modal('请确认删除文件: ' + ev.target.id, () => {
          if (this_.event_listener != null)
            this_.event_listener('delete', ev.target.id);
        });
      }
      function add_tr(row_num) {
        var row = this_.data.rows[row_num];
        var tr = document.createElement("tr");
        tbody.appendChild(tr);
        add_text_cell(tr, '' + (row_num + 1), true);
        add_text_cell(tr, row[0], false);
        add_button_cell(tr, row[0], 'x', 'click', delete_file);
      }
      function add_last_tr() {
        var tr = document.createElement("tr");
        tbody.appendChild(tr);
        add_text_cell(tr, '', false);
        add_text_cell(tr, '', false);
        // add_button_cell(tr, 'upload-refresh-button', 'refresh', 'click', refresh_file);
        add_file_cell(tr);
      }
      for (var r  = 0; r < this.data.rows.length; ++ r) {
        add_tr(r);
      }
      if (this.data.rows.length < 20)
        add_last_tr();
    }
  };

  obj.elt = document.createElement("div");
  obj.elt.setAttribute('style', 'margin:10px;');
  return obj;
}

