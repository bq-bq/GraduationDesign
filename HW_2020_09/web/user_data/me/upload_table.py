
# elt
# mounted(config)
# dispose()
# event_listener
# set_data(data_name, data)
# get_data(data_name)
# set_var(var_name, var_)
# get_var(var_name)

from browser import self as window

class upload_table_obj_py:
	def __init__(self):
		self.type_name = 'upload_table'
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
		for field_name in ['文件路径', '操作']:
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
		def add_link_cell(tr, link, text=None):
			td = html.TD()
			tr <= td
			if text is None:
				text = link
			a = html.A(text, **{'href':link})
			td <= a
		def add_button_cell(tr, id, text, event, callback):
			td = html.TD()
			tr <= td
			a = html.BUTTON(text, **{'type':'button', 'class':'btn btn-primary btn-sm', 'id':id})
			td <= a
			a.bind(event, callback)			
		def upload_file(files):
			if files.length == 0: return;
			if files.length >= 20:
				window.error_toast('一次不能上传超过20个文件')
				return
			form_data = window.FormData.new()
			form_data.append('user_info', window.user_info)
			for i,file in enumerate(files):
				# if file.size >= 100000000:
				# 	window.error_toast('文件大小限制: 100MB')
				# 	return
				form_data.append('file'+str(i+1), file)
			xhr = window.XMLHttpRequest.new()
			xhr.open('POST', '/upload', True);
			def onload_callback(ev):
				if xhr.status == 200:
					reply = JSON.parse(xhr.responseText)
					if 'url' in reply:
						if self.event_listener is not None:
							self.event_listener('add', reply['url'])
						window.info_toast('已上传' + str(files.length) + '个文件')
						return
					if 'error' in reply:
						window.error_toast('上传失败: ' + reply['error'])
				else:
					window.error_toast('上传失败')
			xhr.onload = onload_callback
			xhr.send(form_data)
		def add_file_cell(tr):
			td = html.TD()
			tr <= td
			file = html.INPUT(style={'display':'none'}, **{'type':'file', 'multiple':'multiple', 'name':'file[]'})
			td <= file
			file.bind('change', lambda ev: upload_file(file.files))
			button = html.BUTTON('+', **{'id':'upload-table-submit', 'type':'button', 'class':'btn btn-success btn-sm'})
			td <= button
			button.bind('click', lambda ev: file.click())
		def delete_file(ev):
			def callback(ev2):
				if self.event_listener is not None:
					self.event_listener('delete', ev.target.id)
			window.confirm_modal('请确认删除文件: ' + ev.target.id, callback)
		def add_tr(row_num):
			row = self.data['rows'][row_num]
			tr = html.TR()
			tbody <= tr
			add_text_cell(tr, str(row_num + 1), True)
			add_link_cell(tr, row[0])
			add_button_cell(tr, row[0], 'x', 'click', delete_file)
		def add_last_tr():
			tr = html.TR()
			tbody <= tr
			add_text_cell(tr, '', False)
			add_text_cell(tr, '', False)
			add_file_cell(tr)
		for r in range(len(self.data['rows'])):
			add_tr(r)
		# if len(self.data['rows']) < 20:
		add_last_tr()

