
from browser import self as window

class _ui_table_helper_py:

	def get_data(self, data_name):
		if data_name == 'selected':
			return self._get_selelcted()
		elif data_name == 'data':
			return self._get_data()
		elif data_name == 'text_data':
			return self._get_text_data()
		else:
			window.error_toast('No such data: ' + data_name)

	def set_data(self, data_name, data):
		if data_name == 'selected':
			return self._set_selected(data)
		elif data_name == 'data':
			self.text_data = None
			return self._set_data(data)
		elif data_name == 'text_data':
			return self._set_text_data(data)
		else:
			window.error_toast('No such data: ' + data_name)

	def _get_data(self):
		return self.data

	def _event_listener_data(self):
		if self.event_listener is not None:
			if self.text_data is not None:
				text_data_col = int(self.config['attr']['text_data_col'])
				self.text_data['rows'][0][text_data_col] = JSON.stringify(self.data)
				self.event_listener('change', 'text_data')
			else:
				self.event_listener('change', 'data')
			self.event_listener('change_data', None)

	def _set_selected_row(self, row):
		if self.selected_row == row: return
		self.selected_row = row
		if self.event_listener is not None:
			self.event_listener('change', 'selected')
			selected_text = None
			if hasattr(self, 'key_column'):
				field_names = []
				if 'field_names' in self.data:
					field_names = self.data['field_names']
				if self.key_column is not None and self.key_column in field_names:
					key_column_index = field_names.index(self.key_column)
				else:
					key_column_index = 0
				selected_text = None if row is None else row[key_column_index]			
			self.event_listener('change_selected', selected_text)

	def _recover_selected_row(self, rows, old_rows):
		if self.selected_row is None: return
		old_text = str(self.selected_row)
		for row in rows:
			if old_text == str(row):
				self.selected_row = row
				break
		else:
			if old_rows is not None and self.selected_row in old_rows:
				index = old_rows.index(self.selected_row)
				if index < len(rows):
					selected_row = rows[index]
				else:
					selected_row = None
			else:
				selected_row = None
			self._set_selected_row(selected_row)

	def _selected_cols(self, row):
		selected_cols = (self.config['attr']['selected_cols'] if 'selected_cols' in self.config['attr'] else None)
		if selected_cols is None:
			selected_cols = [i for i in range(min(len(row), len(self.data['field_names'])))]
		else:
			try:
				selected_cols = [int(v) for v in selected_cols]
			except:
				selected_cols = [self.data['field_names'].index(v) for v in selected_cols]
		return selected_cols

	def _set_selected(self, row):
		if self.selected_row is None: return
		row = row['rows'][0]
		selected_cols = self._selected_cols(row)
		for c,v in zip(selected_cols, row):
			self.selected_row[c] = v
		self._set_data(self.data)
		self._event_listener_data()

	def _get_selelcted(self):
		if self.selected_row is None: return None
		field_names = self.data['field_names']
		field_types = self.data['field_types']
		row = self.selected_row
		selected_cols = self._selected_cols(row)
		field_names = [field_names[selected_col] for selected_col in selected_cols]
		field_types = [field_types[selected_col] for selected_col in selected_cols]
		row = [row[c] for c,v in zip(selected_cols,row)]
		return {'field_names':field_names, 'field_types':field_types, 'rows':[row]}

	def _set_text_data(self, text):
		from javascript import JSON
		if text is None:
			self.data = None
			self.text_data = None
		else:
			text_data_col = int(self.config['attr']['text_data_col'])
			self.text_data = text
			text = text['rows'][0][text_data_col].strip()
			if text == '':
				if 'text_data_init' not in self.config['attr']:
					window.error_toast('控件配置中缺少 text_data_init')
				else:
					text_data_init = self.config['attr']['text_data_init']
					self.data = JSON.parse(text_data_init)
					self._set_data(self.data)
			else:
				self.data = JSON.parse(text)
				self._set_data(self.data)

	def _get_text_data(self):
		return self.text_data





def _remove_elt_class(elt, c):
	cs = set(elt.attrs['class'].split())
	if c in cs: cs.remove(c)
	elt.attrs['class'] = ' '.join(cs)

def _add_elt_class(elt, c):
	cs = set(elt.attrs['class'].split())
	cs.add(c)
	elt.attrs['class'] = ' '.join(cs)

class ui_select_panel_py(_ui_table_helper_py):
	def __init__(self):
		self.type_name = 'select_panel'
		self.data = None
		self.selected_row = None
		self.event_listener = None
		self.expandable = 'true'
		self.item_name = None
		self.width = '130px'
		self.key_column = None
		self.selected_cols = None
		self.elt = html.DIV(**{'class':'smooth-scroll', 'overflow':'auto'})
		self.item_color = 'list-group-item-light'
		self.item_color_add = 'list-group-item-secondary'
		self.item_color_selected = 'list-group-item-info'

	def use_example_data(self):
		self.data = {'field_names':['item_name','item_data'], 'field_types':['text','text'], 'rows':[['选项1',''],['选项2','']]}

	def mounted(self, config, is_editing, edit_listener):
		self.config = config
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
			else:
				self.key_column = None
		self._set_data(self.data)

	def set_config(self, config):
		self.mounted(config, None, None)

	def _set_data(self, data):
		self.elt.clear()
		self.elt.style['width'] = self.width
		old_data = self.data
		self.data = None
		if data is None or 'rows' not in data or 'field_names' not in data:
			if self.selected_row is not None:
				self._set_selected_row(None)
			return
		self.data = data
		field_names = self.data['field_names']
		rows = self.data['rows']
		# recover selected
		old_rows = None if old_data is None else old_data['rows']
		self._recover_selected_row(rows, old_rows)
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
			for row in rows:
				if row[key_column_index] == name:
					item_name = '项' if self.item_name is None else self.item_name
					window.error_toast('已存在的'+item_name+': '+name)
					return
			row = ['' for i in range(len(field_names))]
			row[key_column_index] = name
			rows.append(row)
			self._set_data(self.data)
			if self.event_listener is not None:
				self.event_listener('change', 'data')
				self.event_listener('change_data', None)
				if self.item_name is not None:
					window.info_toast('已添加'+self.item_name+': ' + name)
			if len(list_group.children) > 2 and select_item(list_group.children[-2]):
				self._set_selected_row(row)
		def on_delete_item(name):		
			for i,row in enumerate(rows):
				if name == row[key_column_index]:
					rows[i:i+1] = []
					self._set_data(self.data)
					if self.event_listener is not None:
						self.event_listener('change', 'data')
						self.event_listener('change_data', None)
						if self.item_name is not None:
							window.info_toast('已删除'+self.item_name+': ' + name)
					break
			else:
				item_name = '项' if self.item_name is None else self.item_name
				window.error_toast('不能删除不存在的'+item_name+': '+name)
		def on_rename_item(name, new_name):		
			for row in rows:
				if row[key_column_index] == new_name:
					item_name = '项' if self.item_name is None else self.item_name
					window.error_toast('不能重命名为已存在的'+item_name+': '+new_name)
					return
			for i,row in enumerate(rows):
				if name == row[key_column_index]:
					row[key_column_index] = new_name
					self._set_data(self.data)
					if self.event_listener is not None:
						self.event_listener('change', 'data')
						self.event_listener('change_data', None)
						if self.item_name is not None:
							window.info_toast('已重命名'+self.item_name+': ' + name + ' -> ' + new_name)
					break
			else:
				item_name = '项' if self.item_name is None else self.item_name
				window.error_toast('不能重命名不存在的'+item_name+': '+name)
		def on_moveup_item(name):		
			for i,row in enumerate(rows):
				if name == row[key_column_index]:
					if i == 0:
						item_name = '项' if self.item_name is None else self.item_name
						window.error_toast('不能上移第一个'+item_name+': '+name)
						return
					rows[i], rows[i-1] = rows[i-1], rows[i]
					self._set_data(self.data)
					if self.event_listener is not None:
						self.event_listener('change', 'data')
						self.event_listener('change_data', None)
						if self.item_name is not None:
							window.info_toast('已上移'+self.item_name+': ' + name)
					break
			else:
				item_name = '项' if self.item_name is None else self.item_name
				window.error_toast('不能上移不存在的'+item_name+': '+name)
		def input_new_component_name():
			image = None
			inputs = [{'type':'text', 'id':'input_text', 'placeholder':''}]
			def callback(d):
				d = d[0].strip()
				dc = [d1.strip() for d1 in d.split('->') if d1.strip() != '']
				if d == '':
					window.error_toast('没有输入')
				elif d[0] == '-':
					d = d[1:].strip()
					on_delete_item(d)
				elif d[0] == '^':
					d = d[1:].strip()
					on_moveup_item(d)
				elif len(dc) == 2:
					on_rename_item(dc[0], dc[1])
				else:
					on_add_item(d)
			item_name = '项' if self.item_name is None else self.item_name
			window.data_modal(image, '请输入新'+item_name+'的名字', inputs, 'OK', callback)
		def add_row(row):
			item = html.LI(row[key_column_index], **{'class':'list-group-item '+self.item_color})
			def onclick(ev):
				if select_item(item):
					self._set_selected_row(row)
			item.bind('click', onclick)
			list_group <= item
		for row in rows:
			add_row(row)
			if row == self.selected_row:
				select_item(list_group.children[-1])
		if self.expandable == 'false': return
		item_name = '项' if self.item_name is None else self.item_name
		add_item = html.LI('+ 添加'+item_name, **{'class':'list-group-item '+self.item_color_add})
		def onclick(ev):
			input_new_component_name()
		add_item.bind('click', onclick)
		list_group <= add_item

	def _set_selected(self, row):
		if self.selected_row is None: return
		index = self.data['rows'].index(self.selected_row)
		if self.key_column is not None:
			if self.key_column in self.data['field_names']:
				key_column_index = self.data['field_names'].index(self.key_column)
			else:
				key_column_index = int(self.key_column)
		else:
			key_column_index = 0
		item_name = self.data['rows'][index][key_column_index]	
		if row is None:
			self.data['rows'][index:index+1] = []
			self._set_data(self.data)
			self._event_listener_data()
			if self.item_name is not None:
				window.info_toast('已删除'+self.item_name+': ' + item_name)
		else:
			super(ui_select_panel_py, self)._set_selected(row)
			if self.item_name is not None:
				window.info_toast('已修改'+self.item_name+': ' + item_name)


