from browser import html, ajax, document
from browser import self as window
from javascript import JSON
import math, copy

def random_string(k):
	from javascript import Math
	letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	text = ''
	for i in range(k):
		text += letter[int(Math.random() * len(letter))]
	return text

def send_ajax_request(obj, method, data, callback):
	global user_info
	def oncomplete(req):
		callback(JSON.parse(req.text) if req.status == 200 else {'error':req.text if req.text != '' else '未能从服务器获取信息'})
	if 'user_info' not in data: data['user_info'] = user_info
	post_data = {'object':obj, 'method':method, 'data': JSON.stringify(data)}
	ajax.post('ajax', data=post_data, oncomplete=oncomplete)

loaded_py_files = set()
def load_py_file(file):
	global loaded_py_files
	if file in loaded_py_files: return
	loaded_py_files.add(file)
	with open(file) as fp:
		content = fp.read()
		exec(content, globals=globals())

user_info = ['', '', '', ''] # user, session_code, app, app_secret
app_info = {'activities':[]}
current_activity = None

def web_init():
	global app_info, user_info
	document["logout"].bind('click', show_login)
	document["login"].bind('click', show_login)
	app = document['title'].text
	app_info['app'] = app
	user_info = ['','',app,'']
	app_info2 = window.location.href.split('?')
	if len(app_info2) > 1:
		app_info2 = app_info2[1].split('&')
		app_info2 = [info.split('=') for info in app_info2]
		app_info2 = {info[0]:info[1] for info in app_info2}
		if 'app_secret' not in app_info2:
			user_info = app_info2['user_info'].split('*')
			user_info = [window.decodeURI(info) for info in user_info]
	refresh_APP()

def show_login(ev):
	global data_hub, user_info
	if data_hub is not None:
		data_hub.onevent('', '', '') # synchronize the modified data of the previous user
		data_hub = None

	app_secret = app_info['app_secret'] = random_string(16)
	window.location.href = '/me?user_info=%s&app_secret=%s' % ('*'.join(user_info), app_secret)

def obj_to_dict(obj):
	for key in obj:
		val = obj[key]

def obj_name(obj):
	if hasattr(obj, 'config') and obj.config is not None:
		if 'tag' in obj.config: return obj.config['tag']
		if 'init' in obj.config: return obj.config['init']
	return obj.__class__.__name__

class DataHub:
	def __init__(self, as_app='', main_hub=False):
		self.dispose()
		self.as_app = as_app # access the database of another app, this functinality is used to access the client's database by the DB app
		self.main_hub = main_hub
	def dispose(self):
		self.components = {} # component_id -> component
		self.data = {} # name -> table_data
		self.data2obj = {} # name -> list of [data_name, ui_component objects]
		self.ref2obj = {} # ref_name -> list of [data_name, ui_component objects]
		self.change = set()
		self.event_queue = []

	def __repr__(self):
		repr = 'data:\n'
		for table_name in self.data: repr += '\t' + table_name + '\n'
		def print_data(data2obj):
			nonlocal repr
			for table_name, obj_ids in data2obj.items():
				repr += '\t' + table_name + '\n'
				for data_name, obj_id in obj_ids:
					obj = self.components[obj_id]
					repr += '\t\t' + data_name + ': ' + obj_name(obj) + '\n'
		repr += 'data2obj\n'
		print_data(self.data2obj)
		repr += 'ref2obj\n'
		print_data(self.ref2obj)
		return repr

	def add_component(self, obj, remove=False):
		if obj.config is None: return
		obj_id = id(obj)
		updates = []
		if 'data' in obj.config:
			data = obj.config['data']
			for data_name, table_name in data.items():
				if remove:
					self.data2obj[table_name].remove((data_name, obj_id))
					if len(self.data2obj[table_name]) == 0:
						del self.data2obj[table_name]
				else:
					if table_name not in self.data2obj:
						self.data2obj[table_name] = set()
					if (data_name, obj_id) in self.data2obj[table_name]:
						window.error_toast(id(self), '重复添加数据 %s (%s,%s)' % (table_name, data_name, obj_name(obj)))
					self.data2obj[table_name].add((data_name, obj_id)) # when data[table_name] is changed, will call obj.set_data(data_name, data[table_name])
					if table_name[0] == '$':
						if table_name in self.data and self.data[table_name] is not None:
							updates.append((obj, data_name, self.data[table_name]))
					else:
						if table_name not in self.data:
							self.data[table_name] = {'__update_time__':-1}
						if len(self.data[table_name]) > 1:
							updates.append((obj, data_name, self.data[table_name]))
		if 'ref' in obj.config:
			ref = obj.config['ref']
			for data_name, var_name in ref.items():
				if remove:
					self.ref2obj[var_name].remove((data_name, obj_id))
					if len(self.ref2obj) == 0:
						del self.ref2obj[var_name]
				else:
					if var_name not in self.ref2obj:
						self.ref2obj[var_name] = set()
					assert (data_name, obj_id) not in self.ref2obj[var_name]
					self.ref2obj[var_name].add((data_name, obj_id)) # when var[var_name] or 5data[var[var_name]] is changed, will call obj.set_data(data_name, data[var[var_name]])
					if var_name in self.data and self.data[var_name] is not None:
						var_value = self.data[var_name]
						table_name = var_value['rows'][0][0]
						if table_name not in self.data:
							self.data[table_name] = {'__update_time__':-1}
						if len(self.data[table_name]) > 1:
							updates.append((obj, data_name, self.data[table_name]))
		if remove:
			del self.components[obj_id]
			obj.event_listener = None
			self._remove_headless_table_data()
		else:
			self.components[obj_id] = obj
			if hasattr(obj, 'set_event_listener'):
				obj.set_event_listener(lambda ev, ev_arg: self.handle_ui_event(obj, ev, ev_arg))

	def _remove_headless_table_data(self):
		in_use = self.data2obj.keys() | self.ref2obj.keys()
		for var_name in self.ref2obj:
			if var_name in self.data and self.data[var_name] is not None and 'rows' in self.data[var_name]:
				in_use.add(self.data[var_name]['rows'][0][0])
		not_in_use = self.data.keys() - in_use
		for table_name in not_in_use:
			del self.data[table_name]

	def remove_component(self, obj):
		self.add_component(obj, remove=True)

	def _update_data(self, obj0, table_name):
		obj_id0 = id(obj0) if obj0 is not None else None
		to_sync = False
		updates = []
		if table_name in self.data2obj:
			for data_name, obj_id in self.data2obj[table_name]:
				if obj_id == obj_id0: continue
				obj = self.components[obj_id]
				updates.append((obj, data_name, self.data[table_name]))
		for var_name in self.ref2obj:
			if var_name not in self.data: continue
			var_data = self.data[var_name]
			if var_data is None or 'rows' not in var_data: continue
			if len(var_data['rows']) == 0 or len(var_data['rows'][0]) == 0: continue
			table_name2 = var_data['rows'][0][0]
			if table_name2 != table_name: continue
			if var_name not in self.ref2obj: continue
			for data_name, obj_id in self.ref2obj[var_name]:
				if obj_id == obj_id0: continue
				obj = self.components[obj_id]
				updates.append((obj, data_name, self.data[table_name]))
		if table_name in self.ref2obj:
			if self.data[table_name] is None:
				table_data = None
			else:
				table_name2 = self.data[table_name]['rows'][0][0]
				if table_name2 not in self.data:
					self.data[table_name2] = {'__update_time__':-1}
					to_sync = True # need to fetch a table whose name is table_name2
				table_data = self.data[table_name2]
			for data_name, obj_id2 in self.ref2obj[var_name]:
				obj2 = self.components[obj_id2]
				updates.append((obj2, data_name, table_data))
		return updates, to_sync

	def update_data(self, obj, table_name):
		updates, to_sync = self._update_data(obj, table_name)
		if len(updates) > 0:
			for obj2, name2, data2 in updates:
				obj2.set_data(name2, data2)
		return to_sync

	def _handle_change_event(self, obj, data_name):
		assert 'tag' in obj.config or 'init' in obj.config, obj.config
		obj_type = obj.config['tag' if 'tag' in obj.config else 'init']
		has_data = False
		to_sync = False
		data = obj.config['data'] if 'data' in obj.config else {}
		ref = obj.config['ref'] if 'ref' in obj.config else {}
		table_name = None
		assert not (data_name in data and data_name in ref), '%s 不能同在 data 与 ref' % data_name
		if data_name in data:
			has_data = True
			table_name = data[data_name]
		if data_name in ref:
			has_data = True
			table_name = ref[data_name]
			table_name_data = self.data[table_name]
			table_name = table_name_data['rows'][0][0]
		if table_name is not None:
			if table_name[0] != '$':
				self.change.add(table_name)
			tb_data = obj.get_data(data_name)
			if table_name[0] == '$':
				self.data[table_name] = tb_data
			else:
				if tb_data is not None:
					update_time = self.data[table_name]['__update_time__']
					self.data[table_name] = tb_data
					self.data[table_name]['__update_time__'] = update_time
				else:
					self.data[table_name]['rows'] = []
			to_sync = self.update_data(obj, table_name)
		return to_sync, has_data

	def handle_ui_event(self, obj, ev, ev_arg):
		to_sync = False
		if ev == 'change': # a special event which notify the DataHub that a data/var with name ev_arg is changed
			to_sync, has_data = self._handle_change_event(obj, ev_arg)
			if not has_data: return
		elif ev == 'delete': # delete data will not be fetched from the server
			if ev_arg in self.data:
				del self.data[ev_arg]
		events = obj.config['events'] if 'events' in obj.config else {}
		if ev in events:
			action = events[ev]
			if action != '':
				self.onevent(action, ev, ev_arg)
			elif to_sync:
				self.onevent('', '', '')

	def onevent(self, action, ev, ev_arg):
		print('EVENT %s %s %s' % (action, str(ev), str(ev_arg)))
		if len(self.event_queue) == 0:
			self.event_queue.append((action, ev, ev_arg))
			self._onevent()
		else:
			if len(self.event_queue) >= 5:
				window.error_toast('网页产生过多事件,将丢弃这些事件')
				return
			window.warning_toast('网页连续产生事件,将把这些事件添加到序列')
			self.event_queue.append((action, ev, ev_arg))

	def _onevent(self):
		action, ev, ev_arg = self.event_queue[0]
		table_names = []
		table_data = []
		for table_name, tb_data in self.data.items():
			assert table_name is not None
			if table_name[0] == '$': continue
			table_names.append(table_name)
			if table_name in self.change:
				table_data.append(tb_data)
			else:
				table_data.append({'__req__':'read', '__update_time__':tb_data['__update_time__']})
		self.change.clear()
		def next_ev():
			self.event_queue = self.event_queue[1:]
			if len(self.event_queue) > 0:
				self._onevent()
			else:
				if self.main_hub: window.hide_spinner_modal()
		def ev_callback(data):
			if 'error' in data:
				if self.main_hub: window.error_toast(data['error'])
			else:
				for table_name, tb_data in data.items():
					if len(tb_data) == 1:
						self.data[table_name]['__update_time__'] = tb_data['__update_time__']
					else:
						self.data[table_name] = tb_data
						self.update_data(None, table_name)
			next_ev()
		if action is None: action = ''
		if ev is None: ev = ''
		if ev_arg is None: ev_arg = ''
		if len(table_names) > 0 or action not in ('', '@同步'):
			req_data = {'action':action, 'event':ev, 'event_arg':ev_arg, 'table_names':table_names, 'table_data':table_data, 'as_app':self.as_app}
			send_ajax_request('event', 'event', req_data, ev_callback)
		else:
			next_ev()

data_hub = None

def show_activity(activity_id):
	global current_activity
	if current_activity == activity_id: return
	if current_activity is not None:
		if document[current_activity].attrs['class'].endswith(' active'):
			document[current_activity].attrs['class'] = document[current_activity].attrs['class'][:-7]
		document['page-'+current_activity[4:]].style.display = 'none'
	current_activity = activity_id
	document[current_activity].attrs['class'] += ' active'
	document['page-'+current_activity[4:]].style.display = 'inline'

def refresh_APP():
	global user_info
	window.show_spinner_modal()
	def app_info_callback(data):
		if 'error' in data:
			window.hide_spinner_modal()
			window.error_toast(data['error'])
		else:
			if 'user' in data and data['user'] == '': user_info[0] = ''
			refresh_UI(data)
	send_ajax_request('login', 'get_app_info', {'app':app_info['app']}, app_info_callback)

def refresh_UI(new_app_info):
	global app_info, current_activity, data_hub, user_info
	user, session_code, app, app_secret = user_info
	window.set_user_name(user)
	window.user_info = '';
	if app in ('me', 'ui', 'elt') and user != '':
		window.user_info = JSON.stringify({'user':user, 'session_code':session_code, 'app':app, 'app_secret':app_secret})
	document["login"].hidden = (user == '')
	document["logout"].hidden = (user != '')

	for activity in app_info['activities']:
		document['nav-'+activity['id']].unbind('click')
	document["main-nav"].clear()
	app_info.update(new_app_info)
	for activity in app_info['activities']:
		a = html.A(activity['name'], **{'id':'nav-'+activity['id'],'class':'nav-link'})
		li = html.LI(a, **{'class':'nav-item'})
		document["main-nav"] <= li
		a.bind('click', lambda ev: show_activity(ev.target.id))
	document["main"].clear()
	client = user_info[0]
	data_hub = DataHub(client if app_info['app'] == 'db' else '', True)
	for i, activity in enumerate(app_info['activities']):
		page = html.DIV(**{'id':'page-'+activity['id']})
		document["main"] <= page
		if activity['ui_json'] == '':
			pass
		else:
			make_ui(JSON.parse(activity['ui_json']), page, data_hub)
		page.style.display = 'none'
	if len(app_info['activities']) > 0:
		current_activity = None
		show_activity('nav-'+app_info['activities'][0]['id'])
		data_hub.onevent('', '', '')
	else:
		window.hide_spinner_modal()

def fix_ui_json(ui_json):
	config = ui_json.get('config', {})
	if 'vars' in config and 'data' in config:
		for var_name, var in config['vars'].items():
			if var_name in config['data']:
				window.error_toast('%s exists as both data and var: data:%s vars:%s' % (var_name, str(config['data']), str(config['vars'])))
			config['data'][var_name] = var
		del config['vars']
	if 'children' in ui_json:
		for child_ui_json in ui_json['children']:
			fix_ui_json(child_ui_json)

def make_ui(ui_json, page, data_hub, add_component=True):
	fix_ui_json(ui_json)
	def make_component1(ui_json):
		obj = make_component(ui_json, False, data_hub)
		obj_children = None
		if 'children' in ui_json and len(ui_json['children']) > 0:
			obj_children = [make_component1(child_ui_json) for child_ui_json in ui_json['children']]
		return obj, obj_children
	obj, obj_children = make_component1(ui_json)
	page <= obj.elt
	obj.mounted(None)
	if add_component:
		data_hub.add_component(obj)
	def set_children(obj, obj_children):
		if obj_children is None or len(obj_children) == 0: return
		children = [obj2 for obj2, _ in obj_children]
		if not hasattr(obj, 'set_children'):
			print(children)
		obj.set_children(children)
		for obj2, obj_children2 in obj_children:
			set_children(obj2, obj_children2)
	set_children(obj, obj_children)
	return obj

def make_component(ui_json, is_editing, data_hub=None):
	try:
		config = ui_json.get('config', {})
		if ui_json['type'] == 'Custom_Component':
			return Custom_Component(config, is_editing)
		if ui_json['type'] == 'UI_Placehoder':
			return UI_Placehoder(is_editing)
		if ui_json['type'] == 'BorderLayout':
			return BorderLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'VerticalBorderLayout':
			return VerticalBorderLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'FlowLayout':
			return FlowLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'VerticalFlowLayout':
			return VerticalFlowLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'GridLayout':
			return GridLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'Accordion':
			return Accordion(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'UI_Source':
			return UI_Source(config, is_editing)
		if ui_json['type'] == 'UI_Editor':
			return UI_Editor(config, is_editing)
		if ui_json['type'] == 'UI_Trash':
			return UI_Trash(is_editing)
		if ui_json['type'] == 'RangeLayout':
			return RangeLayout(config, is_editing, data_hub=data_hub)
		if ui_json['type'] == 'RepeatLayout':
			return RepeatLayout(config, is_editing, ui_json, data_hub=data_hub)
		raise AssertionError('Unknown component type: ' + ui_json['type'])
	except:
		import traceback
		print(traceback.format_exc())
		config = {'__meta__': {'name': '错误', 'tag': 'div', 'text': '错误', 'init': '', 'files': [], 'data': [], 'ref': [], 'events': [], 'class': {}, 'attr': {}, 'style': {}}, 'tag': 'div', 'text': '错误', 'files': [], 'data': {}, 'events': {}, 'ref': {}, 'class': 'alert alert-error', 'style': {}, 'attr': {'role': 'alert'}}
		return Custom_Component(config, is_editing)

def add_class(elt, clazz):
	if isinstance(elt, (tuple, list)):
		for elt1 in elt:
			add_class(elt1, clazz)
	elif isinstance(clazz, (tuple, list)):
		for clazz1 in clazz:
			add_class(elt, clazz1)
	else:
		if 'class' not in elt.attrs:
			elt.attrs['class'] = clazz
			return
		cs = elt.attrs['class'].split(' ')
		cs = [c.strip() for c in cs if len(c.strip()) != 0]
		if clazz not in cs:
			cs.append(clazz)
		elt.attrs['class'] = ' '.join(cs)

def remove_class(elt, clazz):
	if isinstance(elt, (tuple, list)):
		for elt1 in elt:
			remove_class(elt1, clazz)
	elif isinstance(clazz, (tuple, list)):
		for clazz1 in clazz:
			remove_class(elt, clazz1)
	else:
		if 'class' not in elt.attrs: return
		cs = elt.attrs['class'].split(' ')
		cs = [c.strip() for c in cs if len(c.strip()) != 0]
		if clazz in cs:
			cs.remove(clazz)
		elt.attrs['class'] = ' '.join(cs)

def has_class(elt, clazz):
	if 'class' not in elt.attrs: return False
	cs = elt.attrs['class'].split(' ')
	cs = [c.strip() for c in cs if len(c.strip()) != 0]
	return clazz in cs

def _set_config(elt, config, elt_class=''):
	if elt_class is None:
		elt_class = ''
		if 'class' in elt.attrs:
			class0 = elt.attrs['class'].split()
			for c0 in class0:
				if ('__meta__' not in config) or ('class' not in config['__meta__']) or all(c0 not in cs for cs in config['__meta__']['class'].values()):
					elt_class += c0 + ' '
	if 'attr' in config:
		for key, val in config['attr'].items():
			elt.attrs[key] = val
	if 'style' in config:
		elt.attrs['style'] = ' '.join('%s:%s;' % (key, val) for key, val in config['style'].items())
	if 'class' in config:
		clazz = config['class']
		if isinstance(clazz, (tuple, list)):
			clazz = ' '.join([c for c in clazz if c != ''])
		elt_class += clazz
	elt_class = elt_class.strip()
	if len(elt_class) > 0:
		elt.attrs['class'] = elt_class
	if 'text' in config:
		elt.html = config['text']

def copy_config(config, is_editing):
	c = {}
	assert isinstance(config, dict), 'Wrong type: ' + str(config)
	if is_editing:
		c['__meta__'] = config['__meta__']
	if 'tag' in config: c['tag'] = config['tag']
	if 'text' in config: c['text'] = config['text']
	if 'init' in config: c['init'] = config['init']
	if 'files' in config: c['files'] = config['files'].copy()
	if 'data' in config: c['data'] = dict(config['data']).copy()
	if 'ref' in config: c['ref'] = dict(config['ref']).copy()
	if 'events' in config: c['events'] = dict(config['events']).copy()
	if 'class' in config: c['class'] = config['class']
	if 'attr' in config: c['attr'] = dict(config['attr']).copy()
	if 'style' in config: c['style'] = dict(config['style']).copy()
	return c

def wrap_in_card(card_title, parent_elt, car_body_max_height=None):
	if card_title is None:
		card_body = parent_elt
	else:
		card = html.DIV(**{'class':'card'})
		parent_elt <= card
		card_header = html.DIV(card_title, **{'class':'card-header'})
		card_body = html.DIV(**{'class':'card-body'})
		card <= card_header + card_body
	if car_body_max_height is not None:
		card_body_style = {'align':'center', 'overflow':'auto', 'max-height':car_body_max_height}
		card_body.style = '; '.join('%s:%s' % (k, v) for k, v in card_body_style.items())
	return card_body

class UI_Component:
	dragging = None
	mouse_over = None
	selected = None
	def __init__(self, elt, is_editing):
		self.elt = elt
		self.elt.draggable = is_editing
		self.is_editing = is_editing
		self.parent = None
		self.edit_listener = None
		if is_editing:
			self._editing()
	def children(self):
		return []
	def remove_child(self, child, fire_change_event):
		raise NotImplementedError()
	def clone(self):
		raise NotImplementedError()
	def _editing(self):
		def onclick(ev):
			if self is UI_Component.mouse_over and self.edit_listener is not None: # inside UI_Editor
				if UI_Component.selected is not self:
					UI_Component.selected = self
					self.edit_listener('selected', self)
		def dragstart(ev):
			if self is UI_Component.mouse_over:
				if UI_Component.dragging is not None:
					remove_class(UI_Component.dragging.elt, 'drop_source')
				if UI_Component.selected is not None:
					UI_Component.selected = None
					if self.edit_listener is not None:
						self.edit_listener('selected', None)
				UI_Component.dragging = self
				remove_class(self.elt, 'source_draggable')
				add_class(self.elt, 'drop_source')
		def dragend(ev):
			if self is UI_Component.dragging:
				remove_class(self.elt, 'drop_source')
				UI_Component.dragging = None
		def mouseover(ev):
			if not self.elt.draggable: return
			if UI_Component.mouse_over is None or UI_Component.mouse_over is not self:
				if UI_Component.mouse_over is None:
					add_class(self.elt, 'source_draggable')
					UI_Component.mouse_over = self
				elif not self.ancestor_of(UI_Component.mouse_over):
					remove_class(UI_Component.mouse_over.elt, 'source_draggable')
					add_class(self.elt, 'source_draggable')
					UI_Component.mouse_over = self
		def mouseout(ev):
			remove_class(self.elt, 'source_draggable')
			UI_Component.mouse_over = None
		assert self.is_editing
		self.elt.bind('dragstart', dragstart)
		self.elt.bind('dragend', dragend)
		self.elt.bind('mouseover', mouseover)
		self.elt.bind('mouseout', mouseout)
		self.elt.bind('click', onclick)
	def mounted(self, parent):
		self.parent = parent
		if parent is not None:
			self.edit_listener = parent.edit_listener
		return self
	def dispose(self):
		if self.is_editing:
			self.elt.unbind('dragstart')
			self.elt.unbind('dragend')
			self.elt.unbind('mouseover')
			self.elt.unbind('mouseout')
			self.elt.unbind('click')
		for child in self.children():
			child.dispose()
		if hasattr(self, 'data_hub'):
			for child in self.children():
				self.data_hub.remove_component(child)
	def ancestor_of(self, other):
		if self is other: return True
		for child in self.children():
			if child.ancestor_of(other): return True
		return False
	def get_json(self):
		json = {'type':self.__class__.__name__}
		children = self.children()
		if len(children) > 0:
			json['children'] = [child.get_json() for child in children]
		config = self.get_config()
		if config is not None and len(config) > 0:
			json['config'] = config
		return json
	def set_config(self, config, edited=True):
		self.config = copy_config(config, self.is_editing)
		elt_class = '' # classes added by the UI editing framework
		if self.is_editing: elt_class = None
		_set_config(self.elt, config, None)
		if edited and self.edit_listener is not None:
			self.edit_listener('edited', None)
	def get_config(self):
		return self.config if hasattr(self, 'config') else {}

class Custom_Component(UI_Component):
	def __init__(self, config, is_editing):
		self.event_listener = None
		assert 'js_css_files' not in config, config
		files = []
		if 'files' in config:
			files = config['files']
			for file in files:
				if file.endswith('.js') or file.endswith('.css'):
					window.load_js_css_file(file)
				else:
					load_py_file(file)
		assert 'tag' in config or 'init' in config, config
		if 'tag' in config:
			self.obj = None
			elt = html.maketag(config['tag'])()
			def handle_event(event):
				if self.event_listener is not None:
					self.event_listener(event, None)
			for event in config['events']:
				elt.bind(event, lambda ev: handle_event(event))
		else:
			obj = None
			if config['init'] in globals():
				exec('obj = %s()' % config['init'], locals=locals())
			elif config['init'] in window:
				exec('from browser import self as window\nobj = window.%s()' % config['init'], locals=locals())
			if obj is not None:
				self.obj = obj
				elt = obj.elt
			else:
				self.obj = None
				elt = html.DIV('错误: 无控件', **{'class':'alert alert-info', 'role':'alert'})
		super(Custom_Component, self).__init__(elt, is_editing)
		self.set_config(config, False)
		if is_editing:
			self.use_example_data()
	def clone(self):
		c = Custom_Component(self.config, self.is_editing)
		c.set_event_listener(self.event_listener)
		return c
	def mounted(self, parent):
		super(Custom_Component, self).mounted(parent)
		if self.obj is not None and hasattr(self.obj, 'mounted'):
			self.obj.mounted(self.config, self.is_editing, self.edit_listener)
		return self
	def set_event_listener(self, listener):
		self.event_listener = listener
		if self.obj is not None and listener is not None:
			self.obj.event_listener = listener
	def dispose(self):
		if self.obj is not None and hasattr(self.obj, 'dispose'):
			self.obj.dispose()
	def get_json(self):
		json_obj = {'type':'Custom_Component'}
		config = self.get_config()
		if len(config) > 0: json_obj['config'] = config
		return json_obj
	def use_example_data(self):
		if self.obj is None: return
		if hasattr(self.obj, 'use_example_data'):
			self.obj.use_example_data()
	def set_data(self, data_name, data):
		if self.obj is None:
			if not hasattr(self.elt, data_name):
				setattr(self.elt, data_name, data)
			else:
				window.error_toast('Component "%s" has no attribute "%s"' % (self.config['tag'], data_name))
		else:
			if not hasattr(self.obj, 'set_data'):
				window.error_toast('Component "%s" has no function "set_data"' % self.config['init'])
			else:
				self.obj.set_data(data_name, data)
	def get_data(self, data_name):
		if self.obj is None:
			if not hasattr(self.elt, data_name):
				return getattr(self.elt, data_name)
			else:
				window.error_toast('Component "%s" has no attribute "%s"' % (self.config['tag'], data_name))
		else:
			if hasattr(self.obj, 'get_data'):
				return self.obj.get_data(data_name)
			if hasattr(self.obj, 'get_data_json_text'):
				data_json = self.obj.get_data_json_text(data_name)
				if data_json is None: return None
				return JSON.parse(data_json)
			window.error_toast('Component "%s" has no function "get_data" or "get_data_json_text"' % self.config['init'])
		return None
	def set_config(self, config, edited=True):
		if self.obj is None:
			super(Custom_Component, self).set_config(config, edited)
		else:
			self.config = copy_config(config, self.is_editing)
			if hasattr(self.obj, 'set_config'):
				self.obj.set_config(self.config)
			else:
				_set_config(self.obj.elt, config)
			if edited and self.edit_listener is not None:
				self.edit_listener('edited', None)

web_init()

class UI_Placehoder(UI_Component):
	drag_over = None
	def __init__(self, is_editing):
		style = {'text-align':'center'}
		elt = html.DIV(style=style, **{'class':'ui_placehoder'})
		elt.draggable = False
		super(UI_Placehoder, self).__init__(elt, False)
		self.config = {}
		self.is_editing = is_editing
		if not self.is_editing: return
		elt_img = html.maketag('img')(**{'src':'web/lib/icons/true/ios-add-circle-outline.svg', 'width':'28', 'height':'28'})
		elt_img.draggable = False
		elt <= elt_img
		def dragover(ev):
			if UI_Component.dragging is not None:
				if not UI_Component.dragging.ancestor_of(self):
					if UI_Placehoder.drag_over is None or UI_Placehoder.drag_over is not self:
						if UI_Placehoder.drag_over is not None:
							remove_class(UI_Placehoder.drag_over.elt, 'drop_target')
						if not isinstance(self.parent, UI_Source):
							add_class(self.elt, 'drop_target')
							UI_Placehoder.drag_over = self
			ev.preventDefault() # needed
		def dragleave(ev):
			if UI_Component.dragging is not None:
				if not UI_Component.dragging.ancestor_of(self):
					remove_class(self.elt, 'drop_target')
					UI_Placehoder.drag_over = None
			ev.preventDefault()
		def drop(ev):
			if UI_Placehoder.drag_over is not None:
				if self.parent is not None and (UI_Placehoder.dragging.parent.is_editing or isinstance(UI_Placehoder.dragging.parent, UI_Editor)):
					self.parent.child_drop(self)
				if UI_Placehoder.drag_over is not None:
					remove_class(UI_Placehoder.drag_over.elt, 'drop_target')
					UI_Placehoder.drag_over = None
				if UI_Component.dragging is not None:
					remove_class(UI_Component.dragging.elt, 'drop_source')
					UI_Component.dragging = None
			ev.preventDefault()
		self.elt.bind('drop', drop)
		self.elt.bind('dragover', dragover)
		self.elt.bind('dragleave', dragleave)
	def dispose(self):
		if self.is_editing:
			self.elt.unbind('drop')
			self.elt.unbind('dragover')
			self.elt.unbind('dragleave')
	def clone(self):
		return UI_Placehoder(self.is_editing)
	def children(self):
		return []

class FlowLayout(UI_Component): # children classes: (-, -, -) if flow or (col, col, col) if grid
	def __init__(self, config, is_editing, vertical=False, use_grid=False, data_hub=None):
		self.config = copy_config(config, is_editing)
		self.vertical = vertical
		self.use_grid = use_grid
		self.data_hub = data_hub
		if use_grid:
			elt = html.DIV(style=self.config.get('style', {}), **{'class':'row'})
		elif vertical:
			elt = html.DIV(style=self.config.get('style', {}), **{'class':'d-flex align-items-stretch flex-column'})
		else:
			elt = html.DIV(style=self.config.get('style', {}), **{'class':'d-flex align-items-stretch'})
		_set_config(elt, config, None)
		super(FlowLayout, self).__init__(elt, is_editing)
		self._children = []
		self.set_children([])
	def set_children(self, children_):
		for child in self._children:
			child.dispose()
			if self.data_hub is not None:
				self.data_hub.remove_component(child)
		self.elt.clear()
		self._children = list(children_)
		if self.is_editing:
			if len(self._children) == 0 or not isinstance(self._children[-1], UI_Placehoder):
				placeholder = UI_Placehoder(self.is_editing)
				if self.use_grid:
					add_class(placeholder.elt, 'col')
				self._children.append(placeholder)
		else:
			if len(self._children) > 0 and isinstance(self._children[-1], UI_Placehoder):
				self._children = self._children[:-1]
		remove_class([c.elt for c in self._children], ('col', 'flex-grow-1'))
		if self.use_grid:
			for c in self._children:
				add_class(c.elt, 'col')
		for child in self._children:
			self.elt <= child.elt
			child.mounted(self)
			if self.data_hub is not None:
				self.data_hub.add_component(child)

	def clone(self, c=None):
		assert self.is_editing
		if c is None:
			c = FlowLayout(self.config, self.is_editing)
		c.set_children([c.clone() for c in self._children])
		return c
	def children(self):
		return self._children
	def child_drop(self, child):
		assert self.is_editing
		if UI_Component.dragging is None: return
		dragging = UI_Component.dragging
		if dragging.parent is not None:
			dragging = dragging.parent.remove_child(dragging, False)
		remove_class(dragging.elt, ('col', 'flex-grow-1'))
		if self.use_grid:
			add_class(dragging.elt, 'col')
		self._children[-1:-1] = [dragging]
		self.elt.insertBefore(dragging.elt, self._children[-1].elt)
		dragging.mounted(self)
		if self.edit_listener is not None:
			self.edit_listener('edited', None)
	def remove_child(self, child, fire_change_event):
		assert self.is_editing
		self._children.remove(child)
		self.elt.removeChild(child.elt)
		if fire_change_event and self.edit_listener is not None:
			self.edit_listener('edited', None)
		return child

class VerticalFlowLayout(FlowLayout):
	def __init__(self, config, is_editing, data_hub=None):
		super(VerticalFlowLayout, self).__init__(config, is_editing, vertical=True, data_hub=data_hub)
	def clone(self):
		c = VerticalFlowLayout(self.config, self.is_editing)
		return super(VerticalFlowLayout, self).clone(c)

