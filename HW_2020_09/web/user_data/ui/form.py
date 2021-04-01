
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
	assert datum == datum, '不是时间: '+datetime # not a NaN
	return datum / 1000

def _check_type(text, field_type): # field_types[c_num]
	if field_type == 'number':
		try:
			float(text)
		except:
			window.error_toast('"%s"不是数字' % text)
			return False
	if field_type == 'time':
		try:
			convert_datetime_to_timestamp(text)
		except AssertionError as ex:
			window.error_toast(str(ex))
			return False
	if field_type == 'boolean':
		if text.lower() not in ('true', 'false'):
			window.error_toast('"%s"不是真或假' % text)
			return False
	return True



class form_obj_py:
	form_count = 0
	def __init__(self):
		form_obj_py.form_count += 1
		self.form_id = 'form_%d' % form_obj_py.form_count
		self.elt = html.DIV()
		self.data = None
		self.config = None
		self.event_listener = None
	def use_example_data(self):
		self.data = {'field_names':['field_1'], 'field_types':['text'], 'rows':[['data_1']]}
	def mounted(self, config, is_editing, edit_listener):
		self.config = config
		self.set_data(None, self.data)
	def get_data(self, name):
		return self.data
	def set_data(self, name, data):
		self.data = data
		self.set_data_()
	def set_config(self, config):
		self.config = config
		self.set_data_()
	def set_data_(self):
		self.elt.clear()
		if self.data is None: return
		config = self.config
		if 'title' in config['attr']:
			card_style = {'margin':config['style']['margin'], 'width':config['style']['width']}
			card = html.DIV(style=card_style)
			card.attrs['class'] = 'card'
			self.elt <= card
			card <= html.DIV(config['attr']['title'], **{'class':'card-header'})
			form = html.FORM(**{'class':'card-body'})
			card <= form
		else:
			form_style = {s:config['style'][s] for s in ['margin', 'width'] if s in config['style']}
			form = html.DIV(style=form_style)
			self.elt <= form
		field_names = self.data['field_names']
		field_types = self.data['field_types']
		rows = self.data['rows']
		if field_types is not None:
			for i,field_type in enumerate(field_types):
				if field_type != 'time': continue
				for row in rows:
					if isinstance(row[i], (float,int)):
						row[i] = convert_timestamp_to_datetime(row[i])

		if 'field_names' in config['attr']:
			field_names2 = [name.strip() for name in config['attr']['field_names'].split(',') if name.strip() != '']
			for i, (field_name1, field_name2) in enumerate(zip(field_names, field_names2)):
				field_names[i] = field_name2
		select_options = [None] * len(field_names)
		if 'select_options' in config['attr']:
			options = config['attr']['select_options'].strip()
			options = [[o1.strip() for o1 in o.split(',') if len(o1.strip()) > 0] for o in options.split(';')]
			for i, o in enumerate(options):
				if i < len(select_options) and len(o) > 0:
					select_options[i] = o
		data_columns = None
		if 'data_columns' in config['attr']:
			columns = config['attr']['data_columns'].strip()
			if columns != '':
				columns = [c.strip() for c in columns.split(',') if c.strip() != 0]
				if len(columns) > 0:
					data_columns = [int(c) for c in columns]
		size = ''
		if 'size' in config['style']:
			if config['style']['size'] == 'small': size = ' form-control-sm'
			elif config['style']['size'] == 'large': size = ' form-control-lg'
		editable = True
		if 'editable' in config['attr']:
			editable = (config['attr']['editable'] == 'True')
		if len(rows) == 0:
			rows.append(['' for _ in field_names])
		def bind_action(input, event, col):
			input.bind(event, lambda ev: on_change(col, input))
		
		def on_change(i, input):
			text = input.value
			if rows[0][i] == text: return
			if not _check_type(text, field_types[i]): return
			rows[0][i] = text
			if self.event_listener is not None:
				self.event_listener('change', 'data')
				self.event_listener('change', 'var')
		for i, (field_name, data1) in enumerate(zip(field_names, rows[0])):
			if data_columns is not None:
				if i not in data_columns: continue
			form_group = html.DIV(**{'class':'form-group'})
			form <= form_group
			input_id = self.form_id + '_%d'%(i+1)
			label = html.LABEL(field_name, **{'for':input_id})
			form_group <= label
			if select_options[i] is None or not editable:
 				input = html.maketag('input')(**{'type':'text', 'class':'form-control'+size, 'id':input_id, 'required':True, 'aria-describedby':field_name, 'readonly':not editable})
 				if editable: bind_action(input, 'blur', i)
 			else:
 				input = html.maketag('select')(**{'class':'form-control'+size, 'id':input_id, 'aria-describedby':field_name})
 				for o in select_options[i]:
 					option = html.maketag('option')(o)
 					input <= option
 				bind_action(input, 'change', i)
			input.value = data1
			form_group <= input


