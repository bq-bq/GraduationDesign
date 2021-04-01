
from browser import self as window
import javascript

def convert_timestamp_to_datetime(unixtimestamp):
	date = javascript.Date.new(unixtimestamp*1000)
	year = str(date.getFullYear())
	month = ('0'+str(date.getMonth()+1))[-2:]
	day = ('0'+str(date.getDate()))[-2:]
	hours = ('0'+str(date.getHours()))[-2:]
	minutes = ('0'+str(date.getMinutes()))[-2:]
	seconds = ('0'+str(date.getSeconds()))[-2:]
	return year+'-'+month+'-'+day+' '+hours+':'+minutes+':'+seconds

def convert_datetime_to_timestamp(datetime):
	datum = javascript.Date.parse(datetime)
	return datum / 1000


class table_obj:
	def __init__(self):
		self.type_name = 'table'
		self.data = None
		self.text_data = None
		self.editable = False
		self.deletable = False
		self.row_selectable = False
		self.insertable = False
		self.event_listener = None
		self.selected_row = None
		self.elt = html.DIV()

	def mounted(self, config, is_editing, edit_listener):
		self.config = config
		self.editable = (config['attr']['editable'] == 'true')
		self.insertable = ('insertable' in config['attr'] and config['attr']['insertable'] == 'true')
		self.deletable = ('deletable' in config['attr'] and config['attr']['deletable'] == 'true')
		self.row_selectable = ('row_selectable' in config['attr'] and config['attr']['row_selectable'] == 'true')
		self._set_data(self.data)

	def set_config(self, config):
		self.mounted(config, None, None)

	def use_example_data(self):
		self.data = {'field_names':['表项1','表项2'], 'field_types':['text','number'], 'rows':[['行1-列1',100],['行2-列1',200]]}

	def get_data(self, data_name):
		if data_name == 'selected':
			return self._get_selected()
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

	def _set_data(self, data):
		self.elt.clear()
		old_data = self.data
		self.data = None
		if data is None or 'field_names' not in data:
			if self.selected_row is not None:
				self.selected_row = None
				if self.event_listener is not None:
					self.event_listener('change', 'selected')
					self.event_listener('select', None)
					self.event_listener('change_selected', None)
			return
		self.data = data
		field_names = self.data['field_names']
		field_types = (self.data['field_types'] if 'field_types' in self.data else None)
		rows = self.data['rows']
		if field_types is not None:
			for i,field_type in enumerate(field_types):
				if field_type != 'time': continue
				for row in rows:
					if isinstance(row[i], (float,int)):
						row[i] = convert_timestamp_to_datetime(row[i])

		tb = html.TABLE(**{'class':'small table table-sm table-striped table-hover table-responsive table-bordered'})
		self.elt <= tb
		tbody = html.TBODY()
		tb <= tbody

		def check_type(text, c_num):
			if field_types[c_num] == 'number':
				try:
					float(text)
				except:
					window.error_toast('"%s"不是数字' % text)
					return False
			if field_types[c_num] == 'time':
				try:
					convert_datetime_to_timestamp(text)
				except AssertionError as ex:
					window.error_toast(str(ex))
					return False
			if field_types[c_num] == 'boolean':
				if tex.lower() not in ('true', 'false'):
					window.error_toast('"%s"不是日期' % text)
					return False
			return True

		def on_blur(ev):
			r_num, c_num, _ = [int(num) for num in ev.target.id.split(',')]
			row = rows[r_num]
			text = ev.target.text.strip()
			if text == str(row[c_num]): return
			if not check_type(text, c_num): return
			row[c_num] = text
			self._event_listener_data()
				# window.info_toast('已保存修改: '+data.get('table_name', '?'))

		def delete_insert_mouseenter(ev):
			if self.deletable or self.insertable:
				ev.target.children[0].style.display = 'none'
			if self.deletable:
				ev.target.children[1].style.display = 'inline'
				ev.target.children[2].style.display = 'none'
			if self.insertable:
				ev.target.children[3].style.display = 'inline'

		def delete_insert_mouseleave(ev):
			if self.deletable or self.insertable:
				ev.target.children[0].style.display = 'inline'
			if self.deletable:
				ev.target.children[1].style.display = 'none'
				ev.target.children[2].style.display = 'none'
			if self.insertable:
				ev.target.children[3].style.display = 'none'

		def delete_click(ev):
			parent = ev.target.parent
			parent.children[1].style.display = 'none'
			parent.children[2].style.display = 'inline'

		def delete_click_confirmed(ev):
			row_num = int(ev.target.id)
			rows[row_num:row_num+1] = []
			if self.event_listener is not None:
				self._event_listener_data()
				# window.info_toast('已删除行: %d'%(row_num+1))
				self._set_data(self.data)

		def insert_click(ev):
			row_num = int(ev.target.id)
			rows[row_num+1:row_num+1] = [['' for field_name in field_names]]
			if self.event_listener is not None:
				self._event_listener_data()
				# window.info_toast('已插入行: %d'%(row_num+2))
				self._set_data(self.data)

		def add_first_col(td, row_num):
			if row_num >= 0:
				a1 = html.A(str(row_num+1), **{'class':'text-secondary'})
			else:
				a1 = html.SPAN()
			if self.deletable and row_num != -1:
				a2 = html.SPAN('-', style={'display':'none'}, **{'class':'badge badge-danger'})
				a3 = html.SPAN('请确认删除', style={'display':'none'}, **{'id':str(row_num), 'class':'badge badge-danger'})
			else:
				a2 = html.SPAN()
				a3 = html.SPAN()
			if self.insertable:
				a4 = html.SPAN('+', style={'display':'none','margin-left':'2px'}, **{'id':str(row_num), 'class':'badge badge-success'})
			else:
				a4 = html.SPAN()
			td <= a1+a2+a3+a4
			if self.deletable or self.insertable:
				td.bind('mouseenter', delete_insert_mouseenter)
				td.bind('mouseleave', delete_insert_mouseleave)
			if self.deletable:
				a2.bind('click', delete_click)
				a3.bind('click', delete_click_confirmed)
			if self.insertable:
				a4.bind('click', insert_click)
			return td

		prev_selected_tr = None # if prev_selected_tr is None, prev_selected_row_num is invalid
		prev_selected_row_num = None
		select_cell_0 = None
		select_cell_1 = None
		select_cell_12 = None
		select_cell_2 = None

		def select_row(ev):
			nonlocal prev_selected_tr, prev_selected_row_num, select_cell_1, select_cell_2
			try:
				row_num = int(ev.target.id.split(',')[0])
				prev_selected_row_num = row_num
			except:
				return
			if row_num >= len(rows): return # the +/- buttons will also trigger this event
			tr = ev.target
			while not isinstance(tr, html.TR):
				tr = tr.parent
			if prev_selected_tr is not None:
				prev_selected_tr.className = ''
			prev_selected_row = self.selected_row
			if select_cell_1 is None and select_cell_2 is None:
				prev_selected_tr = tr
				tr.className = 'table-info'
				self.selected_row = rows[row_num]
			else:
				self.selected_row = None
				prev_selected_tr = None
				tr.className = ''
			if prev_selected_row != self.selected_row and self.event_listener is not None:
				self.event_listener('change', 'selected')
				self.event_listener('change_selected', None)
				self.event_listener('select', None)

		def set_select_td_class(cls):
			nonlocal select_cell_1, select_cell_12, tbody
			if select_cell_1 is None or select_cell_12 is None: return
			x1 = min(select_cell_1[0], select_cell_12[0])
			x2 = max(select_cell_1[0], select_cell_12[0])
			y1 = min(select_cell_1[1], select_cell_12[1])
			y2 = max(select_cell_1[1], select_cell_12[1])
			for x in range(x1,x2+1):
				tr = tbody.children[x]
				for y in range(y1,y2+1):
					td = tr.children[y+1]
					td.className = cls
		def select_mousedown(ev):
			nonlocal select_cell_1, select_cell_2
			set_select_td_class('')
			try:
				row_num, col_num, _ = [int(i) for i in ev.target.id.split(',')]
				select_cell_1 = [row_num, col_num]
				select_cell_2 = None
			except:
				pass
		def select_mouseup(ev):
			nonlocal select_cell_1, select_cell_2, select_cell_0
			try:
				if select_cell_1 is None: return
				row_num, col_num, _ = [int(i) for i in ev.target.id.split(',')]
				select_cell_2 = [row_num, col_num]
				select_cell_0 = select_cell_1
				if select_cell_1 == select_cell_2:
					set_select_td_class('')
					select_cell_1 = select_cell_2 = None
			except:
				pass
		def select_mouseenter(ev):
			nonlocal select_cell_1, select_cell_2, select_cell_12, prev_selected_tr
			if select_cell_1 is None or select_cell_2 is not None: return
			set_select_td_class('')
			if prev_selected_tr is not None:
				prev_selected_tr.className = ''
				prev_selected_tr = None
			try:
				row_num, col_num, _ = [int(i) for i in ev.target.id.split(',')]
				select_cell_12 = [row_num, col_num]
				set_select_td_class('table-info')
			except:
				pass

		def on_paste(ev):
			nonlocal select_cell_0,tbody
			if select_cell_0 is not None:
				row_num, col_num = select_cell_0
				text = ev.clipboardData.getData('Text')
				text = [t for t in text.split('\n') if t.strip() != '']
				for i,t in enumerate(text):
					text[i] = [t1 for t1 in t.split('\t') if t1.strip() != '']
				check_type_failed = False
				for i,text2 in enumerate(text):
					for j,t in enumerate(text2):
						if row_num+i < len(tbody.children) and col_num+1+j < len(tbody.children[row_num+i].children):
							if not check_type(t, col_num+j):
								check_type_failed = True
				if check_type_failed: return
				for i,text2 in enumerate(text):
					for j,t in enumerate(text2):
						if row_num+i < len(tbody.children) and col_num+1+j < len(tbody.children[row_num+i].children):
							tbody.children[row_num+i].children[col_num+1+j].children[0].text = t
							rows[row_num+i][col_num+j] = t
				ev.preventDefault()
				self._event_listener_data()
		def on_copy(ev, cut=False):
			nonlocal select_cell_1, select_cell_2, prev_selected_tr, tbody
			if select_cell_1 is not None and select_cell_2 is not None:
				texts = []
				x1 = min(select_cell_1[0], select_cell_12[0])
				x2 = max(select_cell_1[0], select_cell_12[0])
				y1 = min(select_cell_1[1], select_cell_12[1])
				y2 = max(select_cell_1[1], select_cell_12[1])
				for x in range(x1,x2+1):
					tr = tbody.children[x]
					texts1 = []
					for y in range(y1,y2+1):
						td = tr.children[y+1]
						texts1.append(td.children[0].text)
						if cut: td.children[0].text = ''
					texts.append('\t'.join(texts1))
				texts = '\n'.join(texts)
				ev.clipboardData.setData('Text', texts)
				ev.preventDefault()
		def on_cut(ev):
			on_copy(ev, True)
		def add_tr(row_num, row):
			tr = html.TR(**{'id':str(row_num)})
			if row == self.selected_row:
				tr.Class = 'table-info'
			tbody <= tr
			tr <= add_first_col(html.TD(), row_num)
			for i,c in enumerate(row):
				attrs = {'id':'%d,%d,1'%(row_num,i)}
				if self.editable:
					attrs['contenteditable'] = 'true'
				a = html.A(**attrs)
				a.text = c
				td = html.TD(a, **{'id':'%d,%d,2'%(row_num,i)})
				tr <= td
				a.bind('blur', on_blur)
				if self.editable:
					td.bind('mousedown', select_mousedown)
					td.bind('mouseup', select_mouseup)
					td.bind('mouseenter', select_mouseenter)
					a.bind('paste', on_paste)
					a.bind('copy', on_copy)
					a.bind('cut', on_cut)
			if self.row_selectable:
				tr.bind('click', select_row)

		# table header
		thead = html.THEAD(**{'class':'thead-dark'})
		tb <= thead
		tr = html.TR()
		thead <= tr
		min_width = 0
		if self.insertable: min_width = 28
		if self.deletable: min_width = 23
		if self.insertable and self.deletable: min_width = 40
		tr <= add_first_col(html.TH(style={'min-width':'%dpx'%min_width}), -1)
		for field_name in field_names:
			tr <= html.TH(html.A(field_name))
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
					else:
						self.selected_row = None
				else:
					self.selected_row = None
				if self.event_listener is not None:
					self.event_listener('change', 'selected')
					self.event_listener('change_selected', None)
					self.event_listener('select', None)
		# table body
		for row_num, row in enumerate(rows):
			add_tr(row_num, row)

	def _event_listener_data(self):
		if self.event_listener is not None:
			if self.text_data is not None:
				text_data_col = int(self.config['attr']['text_data_col'])
				self.text_data['rows'][0][text_data_col] = JSON.stringify(self.data)
				self.event_listener('change', 'text_data')
				self.event_listener('change_data', None)
			else:
				self.event_listener('change', 'data')
				self.event_listener('change_data', None)

	def _set_selected(self, row):
		if self.selected_row is None: return
		row = row['rows'][0]
		selected_col = (self.config['attr']['selected_col'] if 'selected_col' in self.config['attr'] else None)
		selected_col = (self.data['field_names'].index(selected_col) if selected_col in self.data['field_names'] else None)
		if selected_col is None:
			for i,v in enumerate(row):
				self.selected_row[i] = v
		else:
			self.selected_row[selected_col] = row[0]
		self._set_data(self.data)
		self._event_listener_data()

	def _get_selected(self):
		if self.selected_row is None: return None
		selected_col = (self.config['attr']['selected_col'] if 'selected_col' in self.config['attr'] else None)
		selected_col = (self.data['field_names'].index(selected_col) if selected_col in self.data['field_names'] else None)
		field_names = self.data['field_names']
		field_types = self.data['field_types']
		row = self.selected_row
		if selected_col is not None:
			field_names = [field_names[selected_col]]
			field_types = [field_types[selected_col]]
			row = [row[selected_col]]
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
				if 'init_text_data' not in self.config['attr']:
					window.error_toast('控件配置中缺少 init_text_data')
				else:
					init_data = self.config['attr']['init_text_data']
					self.data = JSON.parse(init_data)
					self._set_data(self.data)
			else:
				self.data = JSON.parse(text)
				self._set_data(self.data)

	def _get_text_data(self):
		return self.text_data
