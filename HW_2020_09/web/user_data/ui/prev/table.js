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

function convert_timestamp_to_datetime(unixtimestamp) {
  var date = new Date(unixtimestamp*1000);
  var year = date.getFullYear();
  var month = ('0'+date.getMonth()).substr(-2);
  var day = ('0'+date.getDate()).substr(-2);
  var hours = ('0'+date.getHours()).substr(-2);
  var minutes = ('0'+date.getMinutes()).substr(-2);
  var seconds = ('0'+date.getSeconds()).substr(-2);
  var dataTime = year+'-'+month+'-'+day+'-'+' '+hours+':'+minutes+':'+seconds;
  return dataTime
}

function convert_datetime_to_timestamp(datetime) {
  var datum = Date.parse(datetime);
  return datum / 1000;
}

function table_obj_js() {
  var obj = {
    type_name: 'table',
    data: null,
    editable: false,
    appendable: true,
    elt: null,
    event_listener: null,
    last_row: null,

    mounted(config, is_editing, edit_listener) {
      this.editable = (config.attr.editable == 'true');
      this.appendable = (config.attr.appendable == 'true');
      this.set_data(null, this.data);
    },
    set_config(config) {
      this.mounted(config)
    },
    use_example_data() {
      this.data = {'field_names':['表项1','表项2'], 'field_types':['text','number'], 'rows':[['行1-列1',100],['行2-列1',200]]}
    },
    dispose() {
    },
    get_data_json_text(data_name) {
      if (this.data == null) return null;
      data_json = JSON.stringify(this.data);
      return data_json;
    },
    set_data(data_name, data_) {
      this.last_row = null;
      while (this.elt.hasChildNodes()) {
        this.elt.removeChild(this.elt.lastChild);
      };
      this.data = null;
      if (data_ == null || ! ('field_names' in data_))return;
      this.data = data_;
      var tb = document.createElement("table");
      tb.setAttribute("class", "small table table-sm table-striped table-hover table-responsive table-bordered");
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
      this.data.field_names.forEach(field_name => {
        th = document.createElement("th");
        tr.appendChild(th);
        var a = document.createElement("a");
        th.appendChild(a);
        a.text = field_name;
      });
      var this_ = this;
      function add_last_row() {
        if (this_.last_row != null)
          this_.data.rows.push(this_.last_row);
        this_.last_row = [];
        for (var i in this_.data.field_names)
          this_.last_row.push('');
      }
      if (this.editable && this.appendable) add_last_row();
      var field_types = this.data.field_types;
      function add_tr(row_num) {
        var row = this_.last_row;
        if (row_num < this_.data.rows.length)
          row = this_.data.rows[row_num];
        tr = document.createElement("tr");
        tbody.appendChild(tr);      
        td = document.createElement("td");
        tr.appendChild(td);
        var a = document.createElement("a");
        td.appendChild(a);
        a.setAttribute("class", "text-secondary");
        a.text = (row_num < this_.data.rows.length ? '' + (row_num + 1) : '+');
        for (var i = 0; i < row.length; ++ i) {
          td = document.createElement("td");
          tr.appendChild(td);
          a = document.createElement("a");
          td.appendChild(a);
          if (this_.editable) a.setAttribute("contenteditable", "true");
          var field_type = field_types[i];
          if (field_type == 'time') row[i] = convert_timestamp_to_datetime();
          a.text = row[i];
          a.id = row_num + ',' + i;
          a.onblur = ev => {
            var num = ev.target.id.split(',');
            var r_num = parseInt(num[0]);
            var c_num = parseInt(num[1]);
            var old = null;
            if (r_num < this_.data.rows.length)
              old = this_.data.rows[r_num][c_num];
            else
              old = this_.last_row[c_num];
            var text = ev.target.text.trim();
            if (text == old) return;
            if (r_num < this_.data.rows.length)
              this_.data.rows[r_num][c_num] = text;
            else
              this_.last_row[c_num] = text;
            if (this_.appendable) {
              if (r_num == this_.data.rows.length) {
                if (! this_.last_row.every(e => e == '')) {
                  add_last_row();
                  add_tr(this_.data.rows.length);
                }
              }
              else if (r_num == this_.data.rows.length - 1) {
                while (r_num >= 0) {
                  var last2_row = this_.data.rows[r_num];
                  r_num -= 1;
                  if (! last2_row.every(e => e == '')) break;
                  this_.last_row = last2_row;
                  this_.data.rows.pop();
                  tbody.removeChild(tbody.lastChild);
                }
              }
            }
            if (this_.event_listener != null)
              this_.event_listener('change', 'data');
          }
        }
      }
      for (var r  = 0; r < this.data.rows.length; ++ r) {
        add_tr(r);
      }
      if (this_.last_row != null) add_tr(this.data.rows.length);
    },
    set_var(var_name, var_) {},
    get_var(var_name) { return null; }

  };

  obj.elt = document.createElement("div");
  return obj;
}

