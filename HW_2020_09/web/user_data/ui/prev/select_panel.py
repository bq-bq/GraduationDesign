
from browser import self as window

def _remove_elt_class(elt, c):
	cs = set(elt.attrs['class'].split())
	if c in cs: cs.remove(c)
	elt.attrs['class'] = ' '.join(cs)

def _add_elt_class(elt, c):
	cs = set(elt.attrs['class'].split())
	cs.add(c)
	elt.attrs['class'] = ' '.join(cs)

class select_panel_obj:
	def __init__(self):
		self.type_name = 'select_panel'
		self.data = None
		self.selected_row = None
		self.event_listener = None
		self.expandable = 'true'
		self.item_name = '项'
		self.width = '130px'
		self.key_column = None
		self.var_column = None
		self.elt = html.DIV(**{'class':'smooth-scroll', 'overflow':'auto'})
		self.item_color = 'list-group-item-light'
		self.item_color_add = 'list-group-item-secondary'
		self.item_color_selected = 'list-group-item-info'

	def use_example_data(self):
		self.data = {'field_names':['item_name','item_data'], 'field_types':['text','text'], 'rows':[['选项1',''],['选项2','']]}

	def mounted(self, config, is_editing, edit_listener):
		if 'attr' in config:
			attr = config['attr']
			if 'item_name' in attr:
				self.item_name = attr['item_name']
			if 'width' in attr:
				self.width = attr['width']
			if 'expandable' in attr:
				self.expandable = attr['expandable']
			if 'key_column' in attr:
				self.key_column = attr['key_column']
			if 'var_column' in attr:
				self.var_column = attr['var_column']
		self._set_data(self.data)

	def get_data(self, data_name):
		# print('get_data', data_name)
		if data_name == 'selected':
			return self._get_selelcted()
		elif data_name == 'data':
			return self._get_data()
		else:
			window.error_toast('No such data: ' + data_name)

	def set_data(self, data_name, data):
		# print('set_data', data_name)
		if data_name == 'selected':
			return self._set_selelcted(data)
		elif data_name == 'data':
			return self._set_data(data)
		else:
			window.error_toast('No such data: ' + data_name)

	def _get_data(self):
		return self.data

	def _set_data(self, data):
		self.elt.clear()
		self.elt.style['width'] = self.width
		old_data = self.data
		self.data = None
		def set_selected_row(row):
			self.selected_row = row
			if self.event_listener is not None:
				self.event_listener('change', 'selected')
				self.event_listener('select', None)
				# self.event_listener('change', 'selected_row')
		if data is None or 'rows' not in data or 'field_names' not in data:
			if self.selected_row is not None:
				set_selected_row(None)
			return
		self.data = data
		field_names = self.data['field_names']
		rows = self.data['rows']
		# selected
		if self.selected_row is not None:
			old_text = str(self.selected_row)
			for row in rows:
				if old_text == str(row):
					self.selected_row = row
					break
			else:
				if old_data is not None and self.selected_row in old_data['rows']:
					index = old_data['rows'].index(self.selected_row)
					if index < len(rows):
						self.selected_row = rows[index]
						set_selected_row(self.selected_row)
					else:
						set_selected_row(None)
				else:
					set_selected_row(None)
		# elt
		list_group = html.UL(**{'class':'list-group'})
		self.elt <= list_group
		if self.key_column is not None and self.key_column in field_names:
			key_column_index = field_names.index(self.key_column)
		else:
			key_column_index = 0
		selected_item = None
		def select_item(item):
			nonlocal selected_item
			if selected_item == item: return False
			if item is not None:
				_remove_elt_class(item, self.item_color)
				_add_elt_class(item, self.item_color_selected)
			if selected_item is not None:
				_remove_elt_class(selected_item, self.item_color_selected)
				_add_elt_class(selected_item ,self.item_color)
			selected_item = item
			return True
		def on_add_item(name):
			row = ['' for i in range(len(field_names))]
			row[key_column_index] = name
			rows.append(row)
			self._set_data(self.data)
			if self.event_listener is not None:
				self.event_listener('change', 'data')
				window.info_toast('已添加'+self.item_name+': ' + name)
			if len(list_group.children) > 2 and select_item(list_group.children[-2]):
				set_selected_row(row)
		def on_delete_item(name):		
			for i,row in enumerate(rows):
				if name == row[key_column_index]:
					rows[i:i+1] = []
					self._set_data(self.data)
					if self.event_listener is not None:
						self.event_listener('change', 'data')
						window.info_toast('已删除'+self.item_name+': ' + name)
					break
			else:
				window.error_toast('不能删除不存在的'+self.item_name+': '+name)
		def on_moveup_item(name):		
			for i,row in enumerate(rows):
				if name == row[key_column_index]:
					if i == 0:
						window.error_toast('不能上移第一个'+self.item_name+': '+name)
						return
					rows[i], rows[i-1] = rows[i-1], rows[i]
					self._set_data(self.data)
					if self.event_listener is not None:
						self.event_listener('change', 'data')
						window.info_toast('已上移'+self.item_name+': ' + name)
					break
			else:
				window.error_toast('不能上移不存在的'+self.item_name+': '+name)
		def input_new_component_name():
			image = 'web/lib/icons/bootstrap/document-text.svg'
			inputs = [{'type':'text', 'id':'input_text', 'placeholder':''}]
			def callback(d):
				d = d[0].strip()
				if d == '':
					window.error_toast('没有输入')
				elif d[0] == '-':
					d = d[1:].strip()
					on_delete_item(d)
				elif d[0] == '^':
					d = d[1:].strip()
					on_moveup_item(d)
				else:
					on_add_item(d)
			window.data_modal(image, '请输入新'+self.item_name+'的名字', inputs, 'OK', callback)
		def add_row(row):
			item = html.LI(row[key_column_index], **{'class':'list-group-item '+self.item_color})
			def onclick(ev):
				if select_item(item):
					set_selected_row(row)
			item.bind('click', onclick)
			list_group <= item
		for row in rows:
			add_row(row)
			if row == self.selected_row:
				select_item(list_group.children[-1])
		if self.expandable == 'false': return
		add_item = html.LI('+ 添加'+self.item_name, **{'class':'list-group-item '+self.item_color_add})
		def onclick(ev):
			input_new_component_name()
		add_item.bind('click', onclick)
		list_group <= add_item

	def _set_selelcted(self, row):
		if self.selected_row is None: return
		index = self.data['rows'].index(self.selected_row)
		if self.key_column is not None and self.key_column in self.data['field_names']:
			key_column_index = self.data['field_names'].index(self.key_column)
		else:
			key_column_index = 0
		item_name = self.data['rows'][index][key_column_index]	
		if row is None:
			self.data['rows'][index:index+1] = []
			self._set_data(self.data)
			window.info_toast('已删除'+self.item_name+': ' + item_name)
		else:
			if self.var_column is not None and self.var_column.strip() != '':
				var = row['rows'][0][0]
				var_column_index = self.data['field_names'].index(self.var_column)
				if self.selected_row[var_column_index] == var: return
				self.selected_row[var_column_index] = var
			else:
				row = row['rows'][0]
				for i,v in enumerate(row):
					self.selected_row[i] = v
			self._set_data(self.data)
			window.info_toast('已修改'+self.item_name+': ' + item_name)
		if self.event_listener is not None:
			self.event_listener('change', 'data')

	def _get_selelcted(self):
		if self.selected_row is None: return None
		field_names = self.data['field_names']
		field_types = self.data['field_types']
		row = self.selected_row
		if self.var_column is not None:
			selected_col = self.data['field_names'].index(self.var_column)
			field_names = [field_names[selected_col]]
			field_types = [field_types[selected_col]]
			row = [row[selected_col]]
		return {'field_names':field_names, 'field_types':field_types, 'rows':[row]}

