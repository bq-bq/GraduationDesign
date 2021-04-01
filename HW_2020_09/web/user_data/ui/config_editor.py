
def make_dropdown(init_value, choices, callback):
	a = html.A(init_value, **{'class':'dropdown-toggle', 'data-toggle':'dropdown', 
								'aria-haspopup':'true', 'aria-expanded':'false', 
								'id':'config_editor_select_id_1'})
	ll = html.DIV(**{'class':'dropdown-menu', 'aria-labelledby':'config_editor_select_id_1'})
	dropdown = html.TD(a + ll, **{'class':'dropdown'})
	for c in choices:
		li = html.A(c, **{'class':'dropdown-item small'})
		ll <= li
		def on_click(ev):
			a.text = ev.target.text
			callback(ev.target.text)
		li.bind('click', on_click)
	return dropdown

class config_editor_obj:
	def __init__(self):
		self.type_name = 'config_editor'
		self.elt = html.DIV()
		self.event_listener = None
		self.item = None
		self.item_table = None
		self.config_names = []
		self.item_name = ''
		self.key_column = 0
		self.config_column = None
		self.options = []
		self.del_btn = None

	def mounted(self, config, is_editing, edit_listener):
		if 'attr' in config:
			attr = config['attr']
			if 'config_names' in attr:
				self.config_names = attr['config_names'].split(',')
			if 'item_name' in attr:
				self.item_name = attr['item_name']
			if 'key_column' in attr:
				try:
					self.key_column = int(attr['key_column'])
				except:
					pass
			if 'config_column' in attr:
				try:
					self.config_column = int(attr['config_column'])
				except:
					pass
			if 'options' in attr:
				self.options = attr['options'].strip().split(';')
				self.options = [[o.strip() for o in options.strip().split(',') if o.strip() != ''] for options in self.options]
			while len(self.options) < len(self.config_names):
				self.options.append([])


	def use_example_data(self):
		self.item = {'rows':[['名称1']]}
		self.set_data(None, self.item)

	def get_data(self, data_name):
		return self.item

	def set_data(self, data_name, data):
		self.item = None
		self.elt.clear()
		if data is None: return
		self.item = data
		row = self.item['rows'][0]
		tb = html.TABLE(**{'class':'small table table-sm table-hover'})
		self.elt <= tb
		thead = html.THEAD(**{'class':'thead-dark'})
		tb <= thead
		tbody = html.TBODY()
		tb <= tbody
		tr = html.TR()
		thead <= tr
		tr <= html.TH()
		tr <= html.TH(self.item_name+'参数')
		tr <= html.TH('值')
		# name
		a1 = html.A(row[self.key_column], **{'contenteditable':'true'})
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD()
		tr <= html.TD(self.item_name+'名称')
		tr <= html.TD(a1)
		def onblur1(ev):
			nonlocal a1
			text = a1.text.strip()
			if text != row[self.key_column]:
				row[self.key_column] = text
				self.del_btn.text = '删除'+self.item_name+' "'+text+'"'
				if self.event_listener is not None:
					self.event_listener('change', 'item')	
		a1.bind('blur', onblur1)
		# configs
		if len(self.config_names) > 0 and self.config_column is not None and self.config_column < len(row):
			texts = row[self.config_column].split(',')
			while len(texts) < len(self.config_names):
				texts.append('')
			def make_td(i):
				if len(self.options[i]) > 0:
					def callback(option):
						nonlocal texts
						if texts[i] == option: return
						texts[i] = option
						row[self.config_column] = ','.join(texts)
						if self.event_listener is not None:
							self.event_listener('change', 'item')
					return make_dropdown(texts[i], self.options[i], callback)
				else:
					a2 = html.A(texts[i], **{'contenteditable':'true'})
					def onblur2(ev):
						nonlocal texts
						text = a2.text.strip()
						if texts[i] == text: return 
						texts[i] = text
						row[self.config_column] = ','.join(texts)
						if self.event_listener is not None:
							self.event_listener('change', 'item')
					a2.bind('blur', onblur2)
					return html.TD(a2)	
			for i,config_name in enumerate(self.config_names):
				tr = html.TR(**{'class':'table-info'})
				tbody <= tr
				config_name = config_name.split(':')
				if len(config_name) == 1:
					tr <= html.TD()
					tr <= html.TD(config_name[0])
				else:
					tr <= html.TD(html.SPAN(config_name[0], **{'class':'badge badge-info'}))
					tr <= html.TD(config_name[1])
				tr <= make_td(i)
		# delete item
		tr = html.TR(**{'class':'table-info'})
		tbody <= tr
		tr <= html.TD()
		tr <= html.TD()
		td = html.TD()
		tr <= td
		self.del_btn = html.BUTTON('删除'+self.item_name+' "'+row[self.key_column]+'"', style={'font-size':'smaller'}, **{'type':'button', 'class':'btn-sm btn-dark'})
		td <= self.del_btn
		def delete_item(ev):
			self.set_data(None, None)
			self.event_listener('change', 'item')
		def confirm_delete_item(ev):
			from browser import self as window
			window.confirm_modal('请确认删除'+self.item_name+': ' + row[self.key_column], delete_item)
		self.del_btn.bind('click', confirm_delete_item)

