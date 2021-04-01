/*
.mounted()
.distroy()
.set_event_listener(event_listener)
.update_data(data)
.data
.editable
.elt
*/

function create_parse_trees_svg() {
  var obj = {
    type_name: 'parse_trees',
    data: {'rows':[['', '']]},
    editable: true,
    elt: null,
    svg: null,
    font_size: 12,
    text_margin: 2,
    node_margin: 12,
    selected_object: null, // isDraging == (selected_object != null)
    selected_pos: null,
    mouse_moved: false,
    svg_width: 1,
    svg_height1: 1,
    svg_height: 1,
    q_nodes: [],
    p_nodes: [],
    removed_link: null,
    q_node_color: "#67C23A",
    p_node_color: "#E6A23C",
    linked_node_color: "#F56C6C",
    event_listener: null,

    mounted(config, edit_listener) {
      this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      this.svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
      this.elt.appendChild(this.svg);
      var this_ = this
      this.elt.onmousedown = (ev) => { this_.mousedown(ev); }
      this.elt.onmousemove = (ev) => { this_.mousemove(ev); }
      this.elt.onmouseup = (ev) => { this_.mouseup(ev); }
      this.elt.onmouseleave = (ev) => { this_.mouseleave(ev); }
      this.elt.oncontextmenu = () => { return false; }
      this.update_data(this.data);
    },
    distroy() {
      return;
    },
    set_event_listener(event_listener) {
      this.event_listener = event_listener;
    },
    _select_node(x, y, nodes, zero_x, zero_y) {
      if (nodes == null) return null;
      for (var i = 0; i < nodes.length; ++ i) {
        for (var j = 0; j < nodes[i].length; ++ j) {
          var node = nodes[i][j];
          if (x >= node.posX + zero_x && x <= node.posX + zero_x + node.node_width && 
              y >= node.posY + zero_y && y <= node.posY + zero_y + node.node_height) {
            return node;
          }
        }
      }
      return null;
    },
    _find_end_node(nodes, link) {
      if (nodes == null) return null;
      for (var i = 0; i < nodes.length; ++ i) {
        for (var j = 0; j < nodes[i].length; ++ j) {
          var node = nodes[i][j];
          if ('lines_out2' in node && node.lines_out2.indexOf(link) != -1) return node;
          if ('lines_in2' in node && node.lines_in2.indexOf(link) != -1) return node;
        }
      }
      return null;
    },
    _add_link_to_nodes(link, q_node, p_node) {
      var this_ = this;
      var compatible_with_existing_links = function(link) {
        var p_node2 = p_node;
        if (p_node2 == null) p_node2 = this_._find_end_node(this_.p_nodes, link);
        if (p_node2 == null) {
          return true;
        }
        if (! ('lines_in2' in p_node2)) { 
          return true; 
        }
        if (p_node2.lines_in2.length == 0) {
          return true;
        }
        var border_to_any = false;
        var overlap_any = false;
        for (var i = 0; i < p_node2.lines_in2.length; ++ i) {
          var link2 = p_node2.lines_in2[i];
          if (link2 == link) {
            if (p_node2.lines_in2.length == 1) {
              return true;
            }
            continue;
          }
          var q_node2 = this_._find_end_node(this_.q_nodes, link2);
          if (q_node.span[0] == q_node2.span[1] || q_node2.span[0] == q_node.span[1]) {
            border_to_any = true;
          }
          if (! (q_node.span[0] >= q_node2.span[1] || q_node2.span[0] >= q_node.span[1])) {
            overlap_any = true;
          }
        }
        return border_to_any && ! overlap_any;
      }
      if (link == null) {
        var link = document.createElementNS("http://www.w3.org/2000/svg", "line");
        link.setAttribute("stroke", this.linked_node_color);
        link.setAttribute("stroke-width", 3);
        link.setAttribute("stroke-opacity", 0.6);
      }
      if (q_node != null) {
        if (! compatible_with_existing_links(link)) {
          return null;
        }
        if (! ('lines_out2' in q_node)) q_node['lines_out2'] = [];
        q_node.lines_out2.push(link);
        q_node.svg_node.children[0].setAttribute("stroke", this.linked_node_color);
        q_node.svg_node.children[0].setAttribute("fill", this.linked_node_color);
        q_node.svg_node.children[1].setAttribute("stroke", this.linked_node_color);
        link.setAttribute("x1", q_node.posX + 1);
        link.setAttribute("y1", q_node.posY + q_node.node_height - 1);
      }
      if (p_node != null) {
        this.svg.appendChild(link);
        // this.svg.insertBefore(link, this.svg.childNodes[0]);
        if (! ('lines_in2' in p_node)) p_node['lines_in2'] = [];
        p_node.lines_in2.push(link);
        p_node.svg_node.children[0].setAttribute("stroke", this.linked_node_color);
        p_node.svg_node.children[0].setAttribute("fill", this.linked_node_color);
        p_node.svg_node.children[1].setAttribute("stroke", this.linked_node_color);
        link.setAttribute("x2", p_node.posX + 1);
        link.setAttribute("y2", this.svg_height1 + p_node.posY + 1);
        this.removed_link = null;       
      }
      return link;
    },
    _add_removed_link() {
      var svg_link = this.removed_link[1];
      var q_node = this.removed_link[0][0];
      var p_node = this.removed_link[0][1];
      this._add_link_to_nodes(svg_link, q_node, p_node);
    },
    _remove_link(svg_link) {
      var q_node = this._find_end_node(this.q_nodes, svg_link);
      var p_node = this._find_end_node(this.p_nodes, svg_link);
      this._remove_link_from_nodes(svg_link, q_node, p_node);
    },
    _remove_link_from_nodes(svg_link, q_node, p_node) {
      if (q_node != null) {
        q_node.lines_out2.splice(q_node.lines_out2.indexOf(svg_link), 1);
        if (q_node.lines_out2.length == 0) {
          q_node.svg_node.children[0].setAttribute("stroke", this.q_node_color);
          q_node.svg_node.children[0].setAttribute("fill", this.q_node_color);
          q_node.svg_node.children[1].setAttribute("stroke", this.q_node_color);
        }
      }
      if (p_node != null) {
        p_node.lines_in2.splice(p_node.lines_in2.indexOf(svg_link), 1);
        if (p_node.lines_in2.length == 0) {
          p_node.svg_node.children[0].setAttribute("stroke", this.p_node_color);
          p_node.svg_node.children[0].setAttribute("fill", this.p_node_color);
          p_node.svg_node.children[1].setAttribute("stroke", this.p_node_color);
        }
        this.svg.removeChild(svg_link);
        if (q_node != null) {
          this.removed_link = [[q_node, p_node], svg_link];
        }
      }
    },
    _remove_first_link(node) {
      if ('lines_out2' in node && node.lines_out2.length > 0) {
        var link = node.lines_out2[0];
        this._remove_link(link);
      }
      else if ('lines_in2' in node && node.lines_in2.length > 0) {
        var link = node.lines_in2[0];
        this._remove_link(link);
      }
    },

    mousedown(event) {
      var x = event.offsetX;
      var y = event.offsetY;
      if (event.which == 3) {
        var node = this._select_node(x, y, this.p_nodes, 0, this.svg_height1);
        if (node == null) {
          node = this._select_node(x, y, this.q_nodes, 0, 0);
        }
        if (node != null) {
          if (this.removed_link != null) {
            var link_nodes = this.removed_link[0];
            if (link_nodes[0] == node || link_nodes[1] == node) {
              this._add_removed_link();
            }
            else {
              this._remove_first_link(node);
            }
          }
          else {
            this._remove_first_link(node);
          }
          if (this._update_pyfind_parse()) {
            if (this.event_listener != null)
              this.event_listener('changed', null);
          }
          event.preventDefault();
          return false;
        }
      }
      else if (this.selected_object == null) {
        var p_node = this._select_node(x, y, this.p_nodes, 0, this.svg_height1);
        if (p_node != null) {
          this.selected_object = this._add_link_to_nodes(null, null, p_node);
          this.selected_object.setAttribute("x1", x);
          this.selected_object.setAttribute("y1", y);
          this.selected_pos = [x, y];
          this.mouse_moved = false;
          event.preventDefault();
          return false;
        }
      }
      return true;
    },

    mousemove(event) {
      if (! this.editable) return true;
      if (this.selected_object == null) return true; // nothing is being dragged
      var x = event.offsetX;
      var y = event.offsetY;
      var dx = x - this.selected_pos[0];
      var dy = y - this.selected_pos[1];
      q_node = this._select_node(x, y, this.q_nodes, 0, 0);
      q_node0 = this._find_end_node(this.q_nodes, this.selected_object);
      if (q_node != q_node0) {
        this._remove_link_from_nodes(this.selected_object, q_node0, null);
        if (this._add_link_to_nodes(this.selected_object, q_node, null) == null) {
          q_node = null;
        }
      }
      if (q_node == null) {
        this.selected_object.setAttribute("y1", y);
        this.selected_object.setAttribute("x1", x);        
      }
      this.mouse_moved = this.mouse_moved || (dx != 0 || dy != 0);
      this.selected_pos = [x, y];
      // this.selected_object.posX += dx;
      // this.selected_object.posY += dy;
      // this._updateBounds(false);
      event.preventDefault();
      return false;
    },

    _update_pyfind_parse() {
      var this_ = this;
      var update_linked_spans = function() {
        for (var i = 0; i < this_.p_nodes.length; ++ i) {
          for (var j = 0; j < this_.p_nodes[i].length; ++ j) {
            var p_node = this_.p_nodes[i][j];
            if ('linked_span' in p_node) delete p_node['linked_span'];
            if ('lines_in2' in p_node) {
              var span = null;
              for (var k = 0; k < p_node.lines_in2.length; ++ k) {
                var link = p_node.lines_in2[k];
                var q_node = this_._find_end_node(this_.q_nodes, link);
                if (span == null) {
                  span = [q_node.span[0], q_node.span[1]];
                }
                else {
                  span[0] = (span[0] < q_node.span[0] ? span[0] : q_node.span[0]);
                  span[1] = (span[1] > q_node.span[1] ? span[1] : q_node.span[1]);
                }
              }
              if (span != null)
                p_node['linked_span'] = span;
            }
          }
        }
      }
      update_linked_spans();
      var tree = this.p_nodes[0][0];
      var pyfind_parse = this._linearize(tree);
      if (pyfind_parse == this.data.rows[0][1]) return false;
      this.data.rows[0][1] = pyfind_parse;
      return true;
    },

    mouseup(event) {
      if (this.selected_object != null) {
        var q_node = this._find_end_node(this.q_nodes, this.selected_object);
        if (q_node == null) {
          this._remove_link(this.selected_object);
        }
        if (this._update_pyfind_parse()) {
          if (this.event_listener != null)
            this.event_listener('changed', null);
        }
        event.preventDefault();
        this.selected_object = null;
        this.mouse_moved = false;
        return false;
      }
      return true;
      // this._updateBounds(true);
    },

    mouseleave(event) {
      // this.mouseup(event)
      // this.selected_object = null;
      // this.mouse_moved = false;
      // this._updateBounds(true);
    },

    clearSvg() {
      while (this.svg.hasChildNodes()) {
        this.svg.removeChild(this.svg.lastChild);
      };    
    },

    _parse_linearized_trees(text, add_span, filter_none=false) {
      var tokens = text.replace(/\(/g, " ( ").replace(/\)/g, " ) ").trim().split(/\s+/)

      var parse_linked_span = function(label) {
        if (label.indexOf('[', 1) > 0 && label.indexOf(']', 1) == label.length - 1) {
          label = label.split('[');
          label[1] = label[1].substring(0, label[1].length - 1).split(',');
          return label;
        }
        else {
          return [label];
        }
      }

      var _to_has_space_str = function(s) {
        var char_map = {'\\':'\\', 'b':' ', 't':'\t', 'L':'(', 'R':')'};
        var res = ''
        var was_slash = false;
        for (var i = 0; i < s.length; ++ i) {
          var c = s[i];
          if (was_slash) {
            if (c in char_map) {
              res = res + char_map[c];
            }
            else {
              res = res + '\\' + c;
            }
            was_slash = false;
          }
          else {
            if (c == '\\') {
              was_slash = true;
            }
            else {
              was_slash = false;
              res = res + c;
            }
          }
        }
        return res;
      }

      var helper = function(index) {
        var trees = [];

        while (index < tokens.length && tokens[index] == "(") {
          var parent_count = 0
          while (tokens[index] == "(") {
            index += 1;
            parent_count += 1;
          }

          var label = tokens[index];
          index += 1;

          if (tokens[index] == "(") {
            var children_index = helper(index);
            var children = children_index['trees'];
            var index = children_index['index'];
            if (! filter_none || (label != '-NONE-' && children.length > 0)) {
              label = label.split('-')[0];
              label = parse_linked_span(label);
              var node = { 'node_type':'InternalTreebankNode', 'label':label[0], 'children':children };
              if (label.length > 1) {
                node['linked_span'] = label[1];
              }
              trees.push(node);
            }
          }
          else {
            var word = tokens[index]
            index += 1
            if (! filter_none || label != '-NONE-') {
              label = parse_linked_span(label);
              word = _to_has_space_str(word)
              var node = { 'node_type':'LeafTreebankNode', 'tag':label[0], 'word':word };
              if (label.length > 1) {
                node['linked_span'] = label[1];
              }
              trees.push(node);
            }
          }
          while (parent_count > 0) {
            if (tokens[index] != ")") console.log(text + " should be )");
            index += 1;
            parent_count -= 1;
          }
        }

        return {'trees':trees, 'index':index };
      }

      var trees_index = helper(0);
      var trees = trees_index['trees']; 
      var index = trees_index['index'];
      if (trees.length == 0) return null;
      if (index < tokens.length) {
        console.log(tokens[index] + " must have been a ( " + tokens[index - 1]);
      }
      if (trees.length > 1) {
        console.log("Should be a single tree, but get " + trees.length + " trees.");
        for (var i = 0; i < trees.length; ++ i) {
          console.log(this._linearize(trees[i]));
        }
      }
      var tree = trees[0];

      index = 0;
      var add_span_to_nodes = function(node) {
        if (node.node_type == 'LeafTreebankNode') {
          node['span'] = [index, index + 1];
          index += 1;
        }
        else {
          var start = index;
          var children = node['children'];
          for (var i = 0; i < children.length; ++ i) {
            add_span_to_nodes(children[i]);
          }
          node['span'] = [start, index];
        }
      }
      if (add_span) {
        add_span_to_nodes(tree);
      }
      return tree;
    },

    _linearize(node) {
      var _to_no_space_str = function(s) {
        var char_map = {'\\':'\\', ' ':'b', '\t':'t', '(':'L', ')':'R'};
        var res = '';
        for (var i = 0; i < s.length; ++ i) {
          var c = s[i];
          if (! (c in char_map)) {
            res = res + c;
          }
          else {
            res = res + '\\' + char_map[c];
          }
        }
        return res;
      }
      if (node['node_type'] == 'InternalTreebankNode') {
        var text = '(' + node['label'];
        var children = node['children'];
        if ('linked_span' in node) {
          var span = node['linked_span'];
          text += '[' + span[0] + ',' + span[1] + ']';
        }
        for (var i = 0; i < children.length; ++ i) {
          text += ' ' + this._linearize(children[i]);
        }
        return text + ')';
      }
      else {
        var text = '(' + node['tag'];
        if ('linked_span' in node) {
          var span = node['linked_span'];
          text += '[' + span[0] + ',' + span[1] + ']';
        }
        return text + ' ' + _to_no_space_str(node['word']) + ')';
      }
    },

    _iterate_tree(node, nodes=[]) {
      nodes.push(node);
      if (node['node_type'] == 'InternalTreebankNode') {
        var children = node['children'];
        for (var i = 0; i < children.length; ++ i) {
          this._iterate_tree(children[i], nodes);
        }
      }
      return nodes;
    },    

    update_data(data) {
      this.data = data;
      question_parse = data.rows[0][0]
      pyfind_parse = data.rows[0][1]
      this.clearSvg();
      this.q_nodes = null;
      this.p_nodes = null;
      // if (data_ == null) return;
      // if (data_.length == 0) return;
      // var question_parse = data_[0]['question_parse'];
      // var pyfind_parse = data_[0]['pyfind_parse'];
      var question_tree = this._parse_linearized_trees(question_parse, true);
      var pyfind_tree = this._parse_linearized_trees(pyfind_parse, true);

      if (question_tree != null)
        this.q_nodes = this._iterate_tree(question_tree);
      if (pyfind_tree != null)
        this.p_nodes = this._iterate_tree(pyfind_tree);
      // node order
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
      var sort_2d = function(nodes) {
        nodes = topological_sort(nodes, (node1, node2) => {
          if (node1['node_type'] == 'LeafTreebankNode') return false;
          var children = node1['children']
          return children.indexOf(node2) != -1;
        });
        for (var i = 0; i < nodes.length; ++ i) {
          sort(nodes[i], (node1, node2) => {
            return node1['span'][0] - node2['span'][0];
          })
        }
        return nodes;
      }
      if (this.q_nodes != null)
        this.q_nodes = sort_2d(this.q_nodes);
      if (this.p_nodes != null)
        this.p_nodes = sort_2d(this.p_nodes);
      // console.log(question_tree == this.q_nodes[0][0]);
      // console.log(pyfind_tree == this.p_nodes[0][0]);
      this.draw(true);
    },

    draw() {
      this.clearSvg();
      var this_ = this;
      // if (this.q_nodes == null) return;
      var title_height = this.font_size + this.text_margin * 3;

      var max = function(x, y) {
        if (x == null) return y;
        if (y == null) return x;
        return x > y ? x : y;
      };
      var create_svg_nodes = function(nodes, fill_color) {
        for (var i = 0; i < nodes.length; ++ i) {
          for (var j = 0; j < nodes[i].length; ++ j) {
            var node = nodes[i][j];
            var svg_node = document.createElementNS("http://www.w3.org/2000/svg", "g");
            this_.svg.appendChild(svg_node);
            node['svg_node'] = svg_node;
            // title background:
            var title_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            title_rect.setAttribute("x", "0");
            title_rect.setAttribute("y", "0");
            title_rect.setAttribute("height", title_height);
            title_rect.setAttribute("fill", fill_color);
            title_rect.setAttribute("fill-opacity", 0.9);
            title_rect.setAttribute("stroke", fill_color);
            title_rect.setAttribute("stroke-width", "1");
            svg_node.appendChild(title_rect);
            // field rect
            var node_height = title_height + this_.font_size + this_.text_margin * 3 + 1;
            if (! ('word' in node)) node_height = title_height + 1;
            var field_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            field_rect.setAttribute("x", "0px");
            field_rect.setAttribute("y", title_height);
            field_rect.setAttribute("height", node_height - title_height);
            field_rect.setAttribute("fill", "#FFFFFF");
            field_rect.setAttribute("fill-opacity", 0.7);
            field_rect.setAttribute("stroke", fill_color);
            field_rect.setAttribute("stroke-width", "1");
            svg_node.appendChild(field_rect);
            // title
            var title = document.createElementNS("http://www.w3.org/2000/svg", "text");
            title.textContent = (('label' in node) ? node['label'] : node['tag']);
            title.setAttribute("font-size", this_.font_size);
            title.setAttribute("x", this_.text_margin);
            title.setAttribute("y", this_.font_size + this_.text_margin);
            title.setAttribute("fill", "#FFFFFF");
            svg_node.appendChild(title);          
            var node_width = title.getBBox().width + 2 * this_.text_margin;
            if ('word' in node) {      
              // field name
              var text_y = title_height + (this_.font_size + this_.text_margin);
              var field_name = document.createElementNS("http://www.w3.org/2000/svg", "text");
              field_name.textContent = node['word'];
              field_name.setAttribute("font-size", this_.font_size);
              field_name.setAttribute("x", 1 + this_.text_margin);
              field_name.setAttribute("y", text_y);
              field_name.setAttribute("fill", "#000000");
              svg_node.appendChild(field_name);
              node_width = max(node_width, field_name.getBBox().width + 2 * this_.text_margin + 2);
            }
            title_rect.setAttribute( "width", node_width);
            field_rect.setAttribute( "width", node_width);
            node.node_width = node_width;
            node.node_height = node_height;
          }
        }
      }
      if (this.q_nodes != null)
        create_svg_nodes(this.q_nodes, this.q_node_color);
      if (this.p_nodes != null)
        create_svg_nodes(this.p_nodes, this.p_node_color);

      var set_y = function(nodes, zero_y) {
        var current_y = zero_y;
        for (var i = 0; i < nodes.length; ++ i) {
          var level_y = 0;
          for (var j = 0; j < nodes[i].length; ++ j) {
            var node = nodes[i][j];
            // level_y = max(level_y, node.node_height);
          }
          level_y += title_height;
          for (var j = 0; j < nodes[i].length; ++ j) {
            var node = nodes[i][j];
            node.posY = current_y;
          }
          current_y += level_y + this_.node_margin;
        }
        this_.svg_height = max(this_.svg_height, current_y - this_.node_margin + 1);
      }
      this.svg_height = 0;
      if (this.q_nodes != null)
        set_y(this.q_nodes, 0);
      this.svg_height1 = this.svg_height + this.node_margin;
      if (this.p_nodes != null)
        set_y(this.p_nodes, 0);
      var set_x = function(node, start_x) {
        node.posX = start_x;
        if (node.node_type == 'LeafTreebankNode') {
          return node.node_width;
        }
        var children = node['children'];
        var width = 0;
        for (var i = 0; i < children.length; ++ i) {
          var child = children[i];
          width += set_x(child, start_x + width) + this_.node_margin;
        }
        width -= this_.node_margin;
        width = max(width, node.node_width);
        node.posX += Math.round((width - node.node_width) / 2);
        return width;
      }
      if (this.q_nodes != null)
        set_x(this.q_nodes[0][0], 0);
      if (this.p_nodes != null)
        set_x(this.p_nodes[0][0], 0);

      var create_svg_links = function(nodes, color) {
        for (var i1 = 0; i1 < nodes.length; ++ i1) {
          for (var j1 = 0; j1 < nodes[i1].length; ++ j1) {
            var node = nodes[i1][j1];
            if (node.node_type == 'LeafTreebankNode') continue;
            var children = node.children;
            var width = 0;
            for (var i2 = 0; i2 < children.length; ++ i2) {
              var child = children[i2];
              var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
              line.setAttribute("stroke", color);
              line.setAttribute("stroke-width", 3);
              line.setAttribute("stroke-opacity", 0.6);
              this_.svg.insertBefore(line, this_.svg.childNodes[0]);
              if (!('lines_out' in node)) node['lines_out'] = [];
              node.lines_out.push(line);
              if (!('lines_in' in child)) child['lines_in'] = [];
              child.lines_in.push(line);
            }
          }
        }
      };
      if (this.q_nodes != null)
        create_svg_links(this.q_nodes, this.q_node_color);
      if (this.p_nodes != null)
        create_svg_links(this.p_nodes, this.p_node_color);

      if (this.q_nodes != null && this.p_nodes != null) {
        for (var i1 = 0; i1 < this.p_nodes.length; ++ i1) {
          for (var j1 = 0; j1 < this.p_nodes[i1].length; ++ j1) {
            var p_node = this.p_nodes[i1][j1];
            if (! ('linked_span' in p_node)) continue;
            var span1 = p_node.linked_span;
            for (var i2 = 0; i2 < this.q_nodes.length; ++ i2) {
              for (var j2 = 0; j2 < this.q_nodes[i2].length; ++ j2) {
                var q_node = this.q_nodes[i2][j2];
                var span2 = q_node.span;
                if (span1[0] == span2[0] && span1[1] == span2[1]) {
                  this._add_link_to_nodes(null, q_node, p_node);
                }
              }
            }
          }
        }
      }
      this._updateBounds(true);
    },

    _updateBounds(update_min_bounds) {
      if (this.q_nodes == null && this.p_nodes == null) return;
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
      var get_bounds = function(nodes) {
        var min_x = null;
        var min_y = null;
        var max_x = null;
        var max_y = null;
        for (var i = 0; i < nodes.length; ++ i) {
          for (var j = 0; j < nodes[i].length; ++ j) {
            var node = nodes[i][j];
            min_x = min(min_x, node.posX);
            min_y = min(min_y, node.posY);
            max_x = max(max_x, node.posX + node.node_width);
            max_y = max(max_y, node.posY + node.node_height);
          }
        }
        return [min_x, min_y, max_x, max_y];
      }
      var q_bounds = [0, 0, 0, 0];
      if (this.q_nodes != null)
        q_bounds = get_bounds(this.q_nodes);
      var p_bounds = [0, 0, 0, 0];
      if (this.p_nodes != null)
        p_bounds = get_bounds(this.p_nodes);
      var min_x = min(q_bounds[0], p_bounds[0]);
      var max_x = max(q_bounds[2], p_bounds[2]);
      var min_y = q_bounds[1];
      var max_y = q_bounds[3];
      this.svg_width = (update_min_bounds ? max_x - min_x : max_x) + 1;
      this.svg_height1 = (update_min_bounds ? max_y - min_y : max_y) + this.node_margin;
      max_y = this.svg_height1 + p_bounds[3]
      this.svg_height = (update_min_bounds ? max_y - min_y : max_y) + 1;
      this.svg.setAttribute('width', this.svg_width);
      this.svg.setAttribute('height', this.svg_height);

      var update_node_pos = function(nodes, min_x, min_y, zero_x, zero_y) {
        for (var i = 0; i < nodes.length; ++ i) {
          for (var j = 0; j < nodes[i].length; ++ j) {
            var node = nodes[i][j];
            if (update_min_bounds) {
              node.posX -= min_x;
              node.posY -= min_y;
            }
            node.svg_node.setAttribute("transform", "translate(" + (zero_x + node.posX) + ", " + (zero_y + node.posY) +")");
            if ('lines_out' in node) {
              for (var k = 0; k < node.lines_out.length; ++ k) {
                var line = node.lines_out[k];
                line.setAttribute("x1", zero_x + node.posX + node.node_width / 2);
                line.setAttribute("y1", zero_y + node.posY + node.node_height - 1);
              }
            }
            if ('lines_in' in node) {
              for (var k = 0; k < node.lines_in.length; ++ k) {
                var line = node.lines_in[k]
                line.setAttribute("x2", zero_x + node.posX + node.node_width / 2);
                line.setAttribute("y2", zero_y + node.posY + 1);
              }
            }
            if ('lines_out2' in node) {
              for (var k = 0; k < node.lines_out2.length; ++ k) {
                var line = node.lines_out2[k];
                line.setAttribute("x1", zero_x + node.posX + 1);
                line.setAttribute("y1", zero_y + node.posY + node.node_height - 1);
              }
            }
            if ('lines_in2' in node) {
              for (var k = 0; k < node.lines_in2.length; ++ k) {
                var line = node.lines_in2[k];
                line.setAttribute("x2", zero_x + node.posX + 1);
                line.setAttribute("y2", zero_y + node.posY + 1);
              }
            }
          }
        }        
      }
      if (this.q_nodes != null)
        update_node_pos(this.q_nodes, min_x, min_y, 0, 0);
      if (this.p_nodes != null)
        update_node_pos(this.p_nodes, min_x, p_bounds[1], 0, this.svg_height1);

      if (this.selected_pos != null) {
        if (update_min_bounds) {
          this.selected_pos[0] -= min_x;
          this.selected_pos[1] -= min_y;
        }
      }
    },
  };

  obj.elt = document.createElement("div");
  return obj;
}

