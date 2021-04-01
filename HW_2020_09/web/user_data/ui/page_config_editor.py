
def make_dropdown(init_value, choices, callback):
	a = html.A(init_value, **{'class':'dropdown-toggle', 'data-toggle':'dropdown', 
								'aria-haspopup':'true', 'aria-expanded':'false', 
								'id':'page_config_editor_select_id_1'})
	ll = html.DIV(**{'class':'dropdown-menu', 'aria-labelledby':'page_config_editor_select_id_1'})
	dropdown = html.TD(a + ll, **{'class':'dropdown'})
	for c in choices:
		li = html.A(c, **{'class':'dropdown-item small'})
		ll <= li
		def on_click(ev):
			a.text = ev.target.text
			callback(ev.target.text)
		li.bind('click', on_click)
	return dropdown

class page_config_editor_obj_py:
	def __init__(self):
		self.type_name = 'page_config_editor'
		self.elt = html.DIV()
		self.event_listener = None
		self.component = None
		self.del_btn = None
	def use_example_data(self):
		self.elt <= html.DIV(self.type_name, **{'class':'alert alert-info', 'role':'alert'})
	def get_data(self, data_name):
		if self.component is None: return None
		return self.component
	def set_data(self, data_name, data):
		self.component = None
		self.elt.clear()
		if data is None: return
		self.component = data
		component = self.component['rows'][0]
		tb = html.TABLE(**{'class':'small table table-sm table-hover'})
		self.elt <= tb
		thead = html.THEAD(**{'class':'thead-dark'})
		tb <= thead
		tbody = html.TBODY()
		tb <= tbody
		tr = html.TR()
		thead <= tr
		tr <= html.TH()
		tr <= html.TH('页面参数')
		tr <= html.TH('设置值')
		# page name
		a1 = html.A(component[0], **{'contenteditable':'true'})
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD(html.SPAN('page', **{'class':'badge badge-info'}))
		tr <= html.TD('页面名称')
		tr <= html.TD(a1)
		def onblur1(ev):
			nonlocal a1
			text = a1.text.strip()
			if text != component[0]:
				component[0] = text
				self.del_btn.text = '删除页面 "'+text+'"'
				if self.event_listener is not None:
					self.event_listener('change', 'component')	
		a1.bind('blur', onblur1)
		# login option
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD(html.SPAN('page', **{'class':'badge badge-info'}))
		tr <= html.TD('何时显示')
		text2 = component[1].split(',')
		a2 = html.A(text2[1] if len(text2) > 1 else '', **{'contenteditable':'true'})
		def on_login_option():
			nonlocal text2, a2
			text2 = ','.join(text2)
			if component[1] != text2:
				component[1] = text2
				if self.event_listener is not None:
					self.event_listener('change', 'component')
		def callback(option):
			nonlocal text2
			if option == '用户组':
				text2 = [option,a2.text.strip()]
			else:
				text2 = [option]
			on_login_option()
		tr <= make_dropdown(text2[0], ['总是', '登录后', '登录前', '网站作者', '用户组'], callback)
		# user group
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD(html.SPAN('page', **{'class':'badge badge-info'}))
		tr <= html.TD('用户组名')
		tr <= html.TD(a2)
		def onblur2(ev):
			nonlocal text2
			if len(text2) > 1:
				text2[1] = a2.text.strip()
				on_login_option()
		a2.bind('blur', onblur2)
		# delete page
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD()
		tr <= html.TD()
		td = html.TD()
		tr <= td
		self.del_btn = html.BUTTON('删除页面 "'+component[0]+'"', style={'font-size':'smaller'}, **{'type':'button', 'class':'btn-sm btn-dark'})
		td <= self.del_btn
		def delete_page(ev):
			self.set_data(None, None)
			self.event_listener('change', 'component')
		def confirm_delete_page(ev):
			from browser import self as window
			window.confirm_modal('请确认删除页面: ' + component[0], delete_page)
		self.del_btn.bind('click', confirm_delete_page)

