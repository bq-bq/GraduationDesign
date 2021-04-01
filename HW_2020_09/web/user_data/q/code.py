
def remove_html_tag(text):
	import re
	p = re.compile(r'<.*?>')
	return p.sub('', text)

def highlight_text(text, names):
	funs = ['query', 'count', 'nonzero', 'is_max', 'is_min', 'avg', 'min', 'max', 'sum', 'any', 'all', 'none', 'between', 'like']
	args = ['select', 'where', 'order_by', 'desc', 'limit']
	names.sort(key=lambda x: -len(x))
	for n in funs:
		text = text.replace(n, '<span class=text-primary>'+n+'</span>')
	for n in args:
		text = text.replace(n, '<span class=text-info>'+n+'</span>')
	for n in names:
		text = text.replace(n, '<span class=text-success>'+n+'</span>')
	return text

def set_html(node, html):
	from browser import self as window
	selection = window.getSelection()
	caret = 0
	def set_caret(node):
		nonlocal caret
		if node.nodeType == node.TEXT_NODE:
			if node == selection.focusNode:
				caret += selection.focusOffset
				return True
			else:
				caret += len(node.text)
				return False
		else:
			for child in node.childNodes:
				if set_caret(child): return True
			return False
	set_caret(node)
	node.html = html
	selection = window.getSelection()
	def set_caret(node):
		nonlocal caret
		if node.nodeType == node.TEXT_NODE:
			if len(node.text) >= caret:
				selection.collapse(node, caret)
				return True
			else:
				caret -= len(node.text)
				return False
		for child in node.childNodes:
			if set_caret(child): return True
		return False
	set_caret(node)

def make_dropdown(init_value, choices, callback):
	a = html.A(init_value, **{'class':'dropdown-toggle', 'data-toggle':'dropdown', 
								'aria-haspopup':'true', 'aria-expanded':'false', 
								'id':'config_editor_select_id_1'})
	ll = html.DIV(**{'class':'dropdown-menu', 'aria-labelledby':'config_editor_select_id_1'})
	dropdown = html.SPAN(a + ll, **{'class':'dropdown'})
	for c in choices:
		li = html.A(c, **{'class':'dropdown-item small'})
		ll <= li
		def on_click(ev):
			a.text = ev.target.text
			callback(ev.target.text)
		li.bind('click', on_click)
	return dropdown

class code_obj:
	def __init__(self):
		self.text_id = random_string(32)
		self.text_input = html.B(**{'contenteditable':'true', 'class':'flex-grow-1'})
		self.io_badge = html.SPAN(style={'margin-left':'10px'}, **{'class':'badge badge-info'})
		self.input_line = html.DIV(self.text_input + html.SPAN(self.io_badge), **{'class':'alert alert-info d-flex align-items-stretch', 'role':'alert'})
		self.elt = html.DIV()
		self.data = None
		self.names = []

	def use_example_data(self):
		self.data = {'rows':[['查找所有教师的姓名','≪添加','教师姓名']]}
		self.set_data('code', self.data)

	def set_data(self, data_name, data):
		if data_name == 'code':
			self._set_code(data)
		elif data_name == 'names':
			self._set_names(data)

	def _set_code(self, data):
		self.data = data
		self.elt.clear()
		if data is None: return
		text, io_op, io_data = self.data['rows'][0]
		if len(self.io_badge.children) > 0:
			self.io_badge.children[1].children[0].text = io_op
			self.io_badge.children[3].children[0].text = io_data
		self.text_input.html = highlight_text(text, self.names)
		self.elt <= self.input_line
		def on_blur(ev):
			text = self.text_input.text.replace(' ',' ')
			if text == self.data['rows'][0][0]: return
			self.data['rows'][0][0] = text
			if self.event_listener is not None:
				self.event_listener('change', 'code')
		def keyup(ev):
			if hasattr(ev, 'key') and ev.key == 'Meta': return
			text = self.text_input.text
			html = highlight_text(text, self.names)
			set_html(self.text_input, html)
		self.text_input.bind('blur', on_blur)
		self.text_input.bind('keyup', keyup)
		self.text_input.bind('paste', keyup)

	def _set_names(self, data):
		io_op = io_data= ''
		if self.data is not None:
			_, io_op, io_data = self.data['rows'][0]
		self.names = [row[0] for row in data['rows'] if row[0][0] != '@']
		names = [n for n in self.names if '.' not in n]
		choices1 = [' ', '≪更新', '更新≫', '≪添加', '添加≫', '≪赋值', '赋值≫']
		choices2 = [' '] + [n for n in names]
		def callback1(text):
			if self.data is not None:
				self.data['rows'][0][1] = text
				if self.event_listener is not None:
					self.event_listener('change', 'code')
		def callback2(text):
			if self.data is not None:
				self.data['rows'][0][2] = text
				if self.event_listener is not None:
					self.event_listener('change', 'code')
		self.io_badge.clear()
		self.io_badge <= html.B('操作 ', **{'class':'text-secondary'}) + \
						make_dropdown(io_op, choices1, callback1) + \
						html.B('<br>对象 ', **{'class':'text-secondary'}) + \
						make_dropdown(io_data, choices2, callback2)

	def get_data(self, data_name):
		if data_name == 'code':
			return self.data
		assert False, 'No such data: ' + data_name
