
# elt
# mounted(config)
# dispose()
# event_listener
# set_data(data_name, data)
# get_data(data_name)
# set_var(var_name, var_)
# get_var(var_name)

from browser import self as window

class user_list_obj_py:
	def __init__(self):
		self.type_name = 'user_list'
		self.data = {}
		self.elt = html.DIV()
		self.event_listener = None
	def use_example_data(self):
		self.elt.clear()
		self.elt <= html.DIV(self.type_name, style={'margin':'10px'}, **{'class':'alert alert-info', 'role':'alert'})
	def set_data(self, data_name, data_):
		from javascript import JSON
		self.elt.clear()
		self.data = None
		if data_ is None or 'field_names' not in data_: return
		self.data = data_
		tb = html.TABLE(style={'margin':'10px'}, **{'class':'small table table-sm table-striped table-hover table-bordered table-responsive'})
		self.elt <= tb
		thead = html.THEAD(**{'class':'thead-dark'})
		tb <= thead
		tbody = html.TBODY()
		tb <= tbody
		tr = html.TR()
		thead <= tr
		th = html.TH()
		tr <= th
		for field_name in ['用户名', '操作']:
			th = html.TH()
			tr <= th
			th <= html.A(field_name)
		def add_text_cell(tr, text, gray_text):
			td = html.TD()
			tr <= td
			a = html.A(text)
			td <= a
			if gray_text:
				a.attrs['class'] = 'text-secondary'
		def add_button_cell(tr, id, text, event, callback):
			td = html.TD()
			tr <= td
			a = html.BUTTON(text, **{'type':'button', 'class':'btn btn-primary btn-sm', 'id':id})
			td <= a
			a.bind(event, callback)			
		def add_user(ev):
			image = 'web/lib/icons/bootstrap/document-text.svg'
			inputs=[{'type':'text', 'id':'input_user_name_to_add', 'placeholder':''}];
			def callback(d):
				d = d[0].strip()
				if d == '':
					window.error_toast('没有输入')
					return
				if self.event_listener is not None:
					self.event_listener('add', d)
			window.data_modal(image, '请输入新的用户名', inputs, 'OK', callback)
		def add_file_cell(tr):
			td = html.TD()
			tr <= td
			button = html.BUTTON('+', **{'id':'user_list_add_user', 'type':'button', 'class':'btn btn-success btn-sm'})
			td <= button
			button.bind('click', add_user)
		def delete_file(ev):
			def callback(ev2):
				if self.event_listener is not None:
					self.event_listener('delete', ev.target.id)
			window.confirm_modal('请确认删除用户 %s 和相关数据' % ev.target.id, callback)
		def add_tr(row_num):
			row = self.data['rows'][row_num]
			tr = html.TR()
			tbody <= tr
			add_text_cell(tr, str(row_num + 1), True)
			add_text_cell(tr, row[0], False)
			add_button_cell(tr, row[0], 'x', 'click', delete_file)
		def add_last_tr():
			tr = html.TR()
			tbody <= tr
			add_text_cell(tr, '', False)
			add_text_cell(tr, '', False)
			add_file_cell(tr)
		for r in range(len(self.data['rows'])):
			add_tr(r)
		add_last_tr()

