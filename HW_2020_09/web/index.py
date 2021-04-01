
from browser import html, ajax, document
from browser import self as window
from javascript import JSON
import math, copy

################################################################
# communication & data management

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
		# print('loading: ' + file)
		content = fp.read()
		exec(content, globals=globals())

################################################################
# login

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
	# image = 'web/lib/icons/true/ios-body.svg'
	# inputs=[{'type':'text', 'id':'user-name', 'placeholder':'用户名'}, {'type':'password', 'id':'user-pwd', 'placeholder':'密码'}]
	# window.data_modal(image, None, inputs, '登陆/退登', start_login)
	global data_hub, user_info
	if data_hub is not None:
		data_hub.onevent('', '', '') # synchronize the modified data of the previous user
		data_hub = None
	# if app_info['app'] == 'me':

	app_secret = app_info['app_secret'] = random_string(16)
	window.location.href = '/me?user_info=%s&app_secret=%s' % ('*'.join(user_info), app_secret)

################################################################
# daba hub

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
				# if  obj_name(obj) == 'ui_table_py':
				# 	print(id(self), '--> %s %s (%s,%s)' % (('remove' if remove else 'add'), table_name, data_name, obj_name(obj)))
				# 	print(id(self), '----> ', table_name in self.data2obj and (data_name, obj_id) in self.data2obj[table_name])
				if remove:
					self.data2obj[table_name].remove((data_name, obj_id))
					if len(self.data2obj[table_name]) == 0:
						del self.data2obj[table_name]
				else:
					if table_name not in self.data2obj:
						self.data2obj[table_name] = set()
					# assert (data_name, obj_id) not in self.data2obj[table_name], \
					# 	(id(self), 'Repeatedly added data %s (%s,%s)' % (table_name, data_name, obj_name(obj)))
					if (data_name, obj_id) in self.data2obj[table_name]:
						window.error_toast(id(self), '重复添加数据 %s (%s,%s)' % (table_name, data_name, obj_name(obj)))
					self.data2obj[table_name].add((data_name, obj_id)) # when data[table_name] is changed, will call obj.set_data(data_name, data[table_name])
					# update object data
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
					# if (data_name, obj_id) not in self.ref2obj[var_name]:
					assert (data_name, obj_id) not in self.ref2obj[var_name]
					self.ref2obj[var_name].add((data_name, obj_id)) # when var[var_name] or 5data[var[var_name]] is changed, will call obj.set_data(data_name, data[var[var_name]])
					# update object data
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
				# obj.set_data(data_name, self.data[table_name])
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
				# obj.set_data(data_name, self.data[table_name])
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
				# obj2.set_data(data_name, table_data)
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
			# if table_name[0] == '$':
			# 	print('---->', self.data.keys())
			# 	assert len(self.data[table_name]) >= 2, '"%s"仅被一个控件使用' % table_name
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

################################################################
# UI

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
			# print('==>', activity['ui_json'])
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

################################################################
# Components

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
			# ev.dataTransfer.setData("text/plain", ev.target.innerText);			
			if self is UI_Component.mouse_over:
				# UI_Component.mouse_over = None
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
			# if self.selected is self: return
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
		# reset attr, class and style of the 'elt'
		_set_config(self.elt, config, None)
		if edited and self.edit_listener is not None:
			self.edit_listener('edited', None)
	def get_config(self):
		return self.config if hasattr(self, 'config') else {}


class Custom_Component(UI_Component):
	def __init__(self, config, is_editing):
		# self.config = copy_config(config, is_editing)
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
			# attrs = {}
			# attrs.update(self.config['attr'])
			# attrs['style'] = self.config.get('style', {})
			# attrs['class'] = self.config['class']
			# if 'text' in self.config and self.config['text'] != '':
			# 	elt = html.maketag(self.config['tag'])(self.config['text'], **attrs)
			# else:
			# 	elt = html.maketag(self.config['tag'])(**attrs)
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
	# example for UI editing
	def use_example_data(self):
		if self.obj is None: return
		if hasattr(self.obj, 'use_example_data'):
			# window.error_toast('Component "%s" has no function "use_example_data"' % self.config['init']);
			self.obj.use_example_data()
	# data
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


################################################################
# main

web_init()

#imported UI_Placehoder, BorderLayout, VerticalBorderLayout, GridLayout, FlowLayout, VerticalFlowLayout, RangeLayout, RepeatLayout, UI_Editor, UI_Trash

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

#imported BorderLayout, VerticalBorderLayout

class BorderLayout(UI_Component): # children classes: (-, flex-grow-1, -)
	def __init__(self, config, is_editing, vertical=False, data_hub=None):
		self.config = copy_config(config, is_editing)
		self.data_hub = data_hub
		if vertical:
			elt = html.DIV(style=self.config.get('style', {}), **{'class':'d-flex align-items-stretch flex-column'})
		else:
			elt = html.DIV(style=self.config.get('style', {}), **{'class':'d-flex align-items-stretch'})
		super(BorderLayout, self).__init__(elt, is_editing)
		self.set_children([UI_Placehoder(is_editing), UI_Placehoder(is_editing), UI_Placehoder(is_editing)], False)
	def set_children(self, children, dispose=True):
		if dispose:
			for child in self.children():
				child.dispose()
				if self.data_hub is not None:
					self.data_hub.remove_component(child)
		self.elt.clear()
		self.left, self.mid, self.right = children
		remove_class([c.elt for c in children], ('col', 'flex-grow-1'))
		add_class(self.mid.elt, 'flex-grow-1')
		for child in self.children():
			self.elt <= child.elt
			child.mounted(self)
			if self.data_hub is not None:
				self.data_hub.add_component(child)
	def clone(self, c=None):
		if c is None:
			c = BorderLayout(self.config, self.is_editing)
		c.set_children([child.clone() for child in self.children()])
		return c	
	def children(self):
		return [self.left, self.mid, self.right]
	def child_drop(self, child):
		assert self.is_editing
		if UI_Component.dragging is None: return
		dragging = UI_Component.dragging
		if dragging.parent is not None:
			dragging = dragging.parent.remove_child(dragging, False)
		remove_class(dragging.elt, ('col', 'flex-grow-1'))
		assert child in self.children(), 'Not a child'
		child.dispose()
		self.elt.replaceChild(dragging.elt, child.elt)
		dragging.mounted(self)
		if child is self.left:
			self.left = dragging
		elif child is self.mid:
			add_class(dragging.elt, 'flex-grow-1')
			self.mid = dragging
		elif child is self.right:
			self.right = dragging
		if self.edit_listener is not None:
			self.edit_listener('edited', None)
	def remove_child(self, child, fire_change_event):
		assert self.is_editing and child in self.children()
		placeholder = UI_Placehoder(self.is_editing)
		self.elt.replaceChild(placeholder.elt, child.elt)
		if child is self.left:
			self.left = placeholder
		elif child is self.mid:
			add_class(placeholder.elt, 'flex-grow-1')
			self.mid = placeholder
		elif child is self.right:
			self.right = placeholder
		if fire_change_event and self.edit_listener is not None:
			self.edit_listener('edited', None)
		placeholder.mounted(self)
		return child

#imported VerticalBorderLayout

class VerticalBorderLayout(BorderLayout):
	def __init__(self, config, is_editing, data_hub=None):
		super(VerticalBorderLayout, self).__init__(config, is_editing, True, data_hub)
	def clone(self):
		c = VerticalBorderLayout(self.config, self.is_editing)
		return super(VerticalBorderLayout, self).clone(c)

#imported FlowLayout, VerticalFlowLayout, GridLayout

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

#imported VerticalFlowLayout 

class VerticalFlowLayout(FlowLayout):
	def __init__(self, config, is_editing, data_hub=None):
		super(VerticalFlowLayout, self).__init__(config, is_editing, vertical=True, data_hub=data_hub)
	def clone(self):
		c = VerticalFlowLayout(self.config, self.is_editing)
		return super(VerticalFlowLayout, self).clone(c)

#imported GridLayout 

class GridLayout(FlowLayout): 
	def __init__(self, config, is_editing, data_hub=None):
		super(GridLayout, self).__init__(config, is_editing, use_grid=True, data_hub=data_hub)
	def clone(self):
		c = GridLayout(self.config, self.is_editing)
		return super(GridLayout, self).clone(c)

#imported Accordion 

class Accordion(UI_Component):
	accordion_count = 0
	def __init__(self, config, is_editing, data_hub=None):
		Accordion.accordion_count += 1
		self.accordion_id = 'accordion-%d' % Accordion.accordion_count
		elt = html.DIV(**{'class':'accordion', 'id':self.accordion_id})
		super(Accordion, self).__init__(elt, is_editing)		
		self._children = []
		self.data_hub = data_hub
		self.set_config(config, False)
	def set_config(self, config, edited):
		self.config = copy_config(config, self.is_editing)
		style = {'border':'1px', 'border-color':'black', 'button-color':'btn-secondary', 'button-text':'板块1;;板块2'}
		style.update(self.config.get('style', {}))	
		self.config['style'] = style
		self.car_body_max_height = self.config['style'].get('max-height', None)
		accordion_style = ['width', 'border', 'border-color']
		accordion_style = {s:style[s] for s in accordion_style if s in style}
		self.elt.attrs['style'] = '; '.join('%s:%s' % (k, v) for k, v in accordion_style.items())
		self.set_children(self._children, False)
		if edited and self.edit_listener is not None:
			self.edit_listener('edited', None)
	def set_children(self, children_, dispose_old_children=True):
		if dispose_old_children:
			for child in self._children:
				child.dispose()
				if self.data_hub is not None:
					self.data_hub.remove_component(child)
		self.elt.clear()
		self._children = list(children_)
		if self.is_editing:
			if len(self._children) == 0 or not isinstance(self._children[-1], UI_Placehoder):
				self._children.append(UI_Placehoder(self.is_editing))
		else:
			if len(self._children) > 0 and isinstance(self._children[-1], UI_Placehoder):
				self._children = self._children[:-1]
		style = self.config['style']
		button_texts = [s.strip() for s in style['button-text'].split(';;') if s.strip() != '']
		button_colors = [s.strip() for s in style['button-color'].split(';;') if s.strip() != '']
		for i, child in enumerate(self._children):
			card = html.DIV(**{'class':'card'})
			card_id = '%s-%d' % (self.accordion_id, i + 1)
			self.elt <= card
			button = html.BUTTON(button_texts[i % len(button_texts)], style={'box-shadow':'none'}, **{'type':'button', 'class':'btn btn-sm btn-block ' + button_colors[i % len(button_colors)], 'data-toggle':'collapse', 'data-target':'#' + card_id, 'aria-expanded':('true' if self.is_editing else 'false'), 'aria-controls':card_id})
			card <= button
			car_body_style = {'align':'center', 'overflow':'auto'}
			if self.car_body_max_height is not None:
				car_body_style['max-height'] = self.car_body_max_height
			car_body = html.DIV(style=car_body_style, **{'id':card_id, 'class':'collapse', 'data-parent':'#'+self.accordion_id}) 
			card <= car_body
			car_body <= child.elt
			child.mounted(self)
			if self.data_hub is not None:
				self.data_hub.add_component(child)
	def clone(self, c=None):
		assert self.is_editing
		if c is None:
			c = Accordion(self.config, self.is_editing)
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
		self._children[-1:-1] = [dragging]
		self.set_children(self._children, dispose_old_children=False)
		if self.edit_listener is not None:
			self.edit_listener('edited', None)
	def remove_child(self, child, fire_change_event):
		assert self.is_editing
		self._children.remove(child)
		self.set_children(self._children, dispose_old_children=False)
		if fire_change_event and self.edit_listener is not None:
			self.edit_listener('edited', None)
		return child

#imported RangeLayout 

class RangeLayout(UI_Component):
	def __init__(self, config, is_editing, data_hub=None):
		elt = html.DIV()
		super(RangeLayout, self).__init__(elt, is_editing)		
		self.data_hub = data_hub
		self._children = []
		self.data = None
		self.child_data = None
		self.set_config(config, False)
		self.cur_page = 0
	def set_config(self, config, edited):
		self.config = copy_config(config, self.is_editing)
		self.page_size = (self.config['attr']['page-size'] if 'page-size' in self.config['attr'] else 1)
		self.pagination_on_top = (self.config['attr']['pagination-on-top'] == 'True' if 'pagination-on-top' in self.config['attr'] else False)
		if self.page_size == 'ALL':
			self.page_size = None
		else:
			self.page_size = int(self.page_size)
		self.car_body_max_height = self.config['style'].get('max-height', None)
		style = config['style']
		elt_style = ['width', 'padding', 'margin']
		elt_style = {s:style[s] for s in elt_style if s in style}
		self.elt.attrs['style'] = '; '.join('%s:%s' % (k, v) for k, v in elt_style.items())
		self.set_children(self._children, False)
		if edited and self.edit_listener is not None:
			self.edit_listener('edited', None)
	def set_children(self, children_, dispose_old_children=True):
		if dispose_old_children:
			for child in self._children:
				child.dispose()
				if self.data_hub is not None:
					self.data_hub.remove_component(child)
		self._children = list(children_)
		if self.is_editing:
			if len(self._children) == 0 or not isinstance(self._children[-1], UI_Placehoder):
				self._children.append(UI_Placehoder(self.is_editing))
		else:
			if len(self._children) > 0 and isinstance(self._children[-1], UI_Placehoder):
				self._children = self._children[:-1]
		if len(self._children) > 0:
			child = self._children[0]
			if self.data_hub is not None:
				self.data_hub.add_component(child)
		self._update_display()
	def _update_display(self):
		self.elt.clear()
		card_title = (self.config['attr']['card_title'] if 'card_title' in self.config['attr'] else None)
		card_body = wrap_in_card(card_title, self.elt, self.car_body_max_height)
		self.cur_page = 0
		def add_pagination():
			nonlocal card_body
			num_pages = 2 if self.is_editing else 0
			if self.data is not None:
				num_pages = math.ceil(len(self.data['rows']) / self.page_size)
			if num_pages > 1:
				cur_li = None
				prev_li = None
				next_li = None
				li_list = []
				def page_action(page):
					nonlocal prev_li, next_li, cur_li
					if self.cur_page == page: return
					remove_class(prev_li, 'disabled')
					remove_class(next_li, 'disabled')
					remove_class(cur_li, 'active')
					if page == 'prev':
						self.cur_page -= 1
					elif page == 'next':
						self.cur_page += 1
					else:
						self.cur_page = page
					if self.cur_page == 0:
						add_class(prev_li, 'disabled')
					if self.cur_page == num_pages - 1:
						add_class(next_li, 'disabled')
					cur_li = li_list[self.cur_page]
					add_class(cur_li, 'active')
					if not self.is_editing:
						self._update_child_data()
				def bind_action(a, page):
					a.bind('click', lambda ev: page_action(page))
				pagination = html.UL(**{'class':'pagination pagination-sm justify-content-center'})
				card_body <= pagination
				a = html.BUTTON('&laquo;', **{'class':'page-link'})
				prev_li = html.LI(a, **{'class':'page-item'})
				pagination <= prev_li
				bind_action(a, 'prev')
				add_class(prev_li, 'disabled')
				for i in range(num_pages):
					a = html.BUTTON('%d'%(i+1), **{'class':'page-link'})
					li = html.LI(a, **{'class':'page-item'})
					pagination <= li
					bind_action(a, i)
					li_list.append(li)
					if i == 0:
						cur_li = li
						add_class(cur_li, 'active')
				a = html.BUTTON('&raquo;', **{'class':'page-link'})
				next_li = html.LI(a, **{'class':'page-item'})
				pagination <= next_li
				bind_action(a, 'next')
		if self.pagination_on_top and (self.page_size is not None or self.is_editing):
			add_pagination()
		if len(self._children) > 0:
			child = self._children[0]
			card_body <= child.elt
			child.mounted(self)
		if not self.pagination_on_top and (self.page_size is not None or self.is_editing):
			add_pagination()
		if (not self.is_editing) and self.data is None and self.child_data is None:
			self.elt.style['display'] = 'none'
		else:
			self.elt.style['display'] = 'inline'
	def clone(self, c=None):
		assert self.is_editing
		if c is None:
			c = RangeLayout(self.config, self.is_editing)
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
		self.set_children([dragging])
		if self.edit_listener is not None:
			self.edit_listener('edited', None)
	def remove_child(self, child, fire_change_event):
		assert self.is_editing
		self._children.remove(child)
		self.set_children(self._children, dispose_old_children=False)
		if fire_change_event and self.edit_listener is not None:
			self.edit_listener('edited', None)
		return child
	def set_event_listener(self, listener):
		self.event_listener = listener
	def get_data(self, data_name):
		if data_name == 'data':
			return self.data
		else: # child_data
			return self.child_data
	def set_data(self, data_name, data):
		if data_name == 'data':
			self.data = data
			self._update_display()
			self._update_child_data()
		else: # child_data
			self.child_data = data
			if self.page_size is not None:
				start = self.page_size * self.cur_page
				for i, r in enumerate(self.child_data['rows']):
					self.data['rows'][start + i] = r
			else:
				for i, r in enumerate(self.child_data['rows']):
					self.data['rows'][i] = r
			self.event_listener('change', 'data')
			self.event_listener('change_data', None)
	def _update_child_data(self):
		if self.data is None or self.page_size is None:
			self.child_data = self.data
		else:
			start = self.page_size * self.cur_page
			rows = self.data['rows'][start:start+self.page_size]
			self.child_data = {'field_names':self.data['field_names'],
							'field_types':self.data['field_types'],
							'rows':rows}
		self.event_listener('change', 'child_data')

#imported RepeatLayout 

class RepeatLayout(UI_Component):
	def __init__(self, config, is_editing, ui_json=None, data_hub=None):
		elt = html.DIV()
		super(RepeatLayout, self).__init__(elt, is_editing)		
		self._children = []
		self.data = None
		self.child_data = None
		self.ui_json = ui_json
		self.data_hub = data_hub
		self.set_config(config, False)
		assert is_editing or data_hub is not None
	def set_config(self, config, edited):
		self.config = copy_config(config, self.is_editing)
		self.layout_direction = self.config['attr']['layout-direction']
		self.grid_layout = (self.config['attr']['grid-layout'] == 'True')
		style = config['style']
		self.elt.attrs['style'] = '; '.join('%s:%s' % (k, v) for k, v in style.items())
		if self.grid_layout:
			self.elt.attrs['class'] = 'row'
		elif self.layout_direction == 'Vertical':
			self.elt.attrs['class'] = 'd-flex align-items-stretch flex-column'
		else:
			self.elt.attrs['class'] = 'd-flex align-items-stretch'
		self.set_children(self._children, False)
		if edited and self.edit_listener is not None:
			self.edit_listener('edited', None)
	def set_children(self, children_, dispose_old_children=True):
		if dispose_old_children:
			for child in self._children:
				child.dispose()
				if self.data_hub is not None:
					self.data_hub.remove_component(child)
		self._children = list(children_)
		if self.is_editing:
			if len(self._children) == 0:
				self._children.append(UI_Placehoder(self.is_editing))
		else:
			if len(self._children) > 0 and isinstance(self._children[-1], UI_Placehoder):
				self._children = self._children[:-1]
		self.elt.clear()
		if self.is_editing:
			self.elt <= html.DIV('控件重复器', style={'color':'grey'}, **{'class':"text-center h6 small"})
		for child in self._children:
			remove_class(child.elt, ('col', 'flex-grow-1'))
			if self.grid_layout:
				add_class(child.elt, 'col')
			self.elt <= child.elt
			child.mounted(self)
			if self.data_hub is not None:
				self.data_hub.add_component(child)
	def clone(self, c=None):
		assert self.is_editing
		if c is None:
			c = RepeatLayout(self.config, self.is_editing)
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
		self.set_children([dragging])
		if self.edit_listener is not None:
			self.edit_listener('edited', None)
	def remove_child(self, child, fire_change_event):
		assert self.is_editing
		self._children.remove(child)
		self.set_children(self._children, dispose_old_children=False)
		if fire_change_event and self.edit_listener is not None:
			self.edit_listener('edited', None)
		return child
	def set_event_listener(self, listener):
		self.event_listener = listener

	def get_data(self, data_name):
		if data_name == 'data':
			return self.data
		else: # child_data
			return self.child_data[data_name]
	def set_data(self, data_name, data):
		def remove_prev_var():
			to_remove = []
			for var in self.config['data']:
				if var != 'child_data' and var.startswith('child_data'):
					to_remove.append(var)
			for var in to_remove:
				del self.config['data'][var]
		if data_name == 'data':
			self.data = data
			self.child_data = {}
			children = []
			child_data_prefix = None
			if 'child_data' in self.config['data']:
				child_data_prefix = self.config['data']['child_data']
			if child_data_prefix is not None and len(self.ui_json['children']) > 0:
				self.data_hub.remove_component(self)
				remove_prev_var()
				def change_var(ui_json, prefix, name):
					to_change = []
					if 'config' in ui_json:
						for var_name, var_data_name in ui_json['config']['data'].items():
							if var_data_name == prefix: to_change.append(var_name)
					for var_name in to_change:
						ui_json['config']['data'][var_name] = name
					if 'children' in ui_json:
						for child_ui_json in ui_json['children']:
							change_var(child_ui_json, prefix, name)
				child_ui_json = self.ui_json['children'][0]
				rows = [] if self.data is None else self.data['rows']
				for i,row in enumerate(rows):
					print('%d/%d'%(i+1,len(rows)))
					child_var = 'child_data#%d'%i
					child_data_name = child_data_prefix + ('#%d'%i)
					child_data = {'field_names':data['field_names'], 'field_types':data['field_types'], 'rows':[row]}
					self.child_data[child_var] = child_data
					self.config['data'][child_var] = child_data_name
					ui_json = copy.deepcopy(child_ui_json)
					change_var(ui_json, child_data_prefix, child_data_name)
					child = make_ui(ui_json, self.elt, self.data_hub, False)
					children.append(child)
				self.data_hub.add_component(self)
				self.set_children(children)
				for child_data_name in self.child_data:
					self.event_listener('change', child_data_name)
			# print(self.data_hub)
		else: # child_data
			if data_name in self.child_data:
				row = self.child_data[data_name]['rows'][0]
				for i,v in enumerate(data['rows'][0]):
					row[i] = v
				self.event_listener('change', 'data')
				self.event_listener('change_data', None)

#imported UI_Trash 

class UI_Trash(UI_Component):
	def __init__(self, is_editing):
		ph = UI_Placehoder(True)
		img = ph.elt.children[0]
		img.attrs['src'] = 'web/lib/icons/true/ios-trash.svg'
		img.attrs['style'] = 'width:64px; height:64px;'
		# add_class(ph.elt, 'float-right')
		super(UI_Trash, self).__init__(ph.elt, True)
		if not is_editing:
			ph.elt.draggable = False
		ph.mounted(self)
		self.config = None
	def child_drop(self, child):
		if UI_Component.dragging is None: return
		dragging = UI_Component.dragging
		if dragging.parent is not None:
			dragging = dragging.parent.remove_child(dragging, True)
			dragging.dispose()
	def clone(self):
		return UI_Trash(True)

#imported UI_Source

def get_source_ui_json(config_template):
	config = {'__meta__':config_template}
	type_ = 'Custom_Component'
	if 'tag' in config_template and config_template['tag'].strip() != '':
		config['tag'] = config_template['tag']
		if config_template['tag'].startswith('#') or config_template['tag'].startswith('$'):
			type_ = config_template['tag'][1:]
	if 'text' in config_template and config_template['text'].strip() != '':
		config['text'] = config_template['text']
	if 'init' in config_template and config_template['init'].strip() != '':
		config['init'] = config_template['init']
	if 'files' in config_template:
		config['files'] = config_template['files']
	config['data'] = {}
	config['ref'] = {}
	config['events'] = {}
	if 'class' in config_template:
		c = ' '.join(value[0].strip() for _, value in config_template['class'].items() if value[0].strip() != '')
		if c.strip() != '': config['class'] = c.strip()
	if 'style' in config_template:
		config['style'] = {name.strip():value[0].strip() for name, value in config_template['style'].items() if len(value) > 0 and value[0].strip() != ''}
	if 'attr' in config_template:
		config['attr'] = {name.strip():value[0].strip() for name, value in config_template['attr'].items() if len(value) > 0 and value[0].strip() != ''}
	return {'type':type_, 'config':config}

class UI_Source(Custom_Component):
	def __init__(self, config, is_editing=False):
		self.config = copy_config(config, is_editing)
		self.event_listener = None
		elt = html.DIV(style={'padding':'3px'}, **{'class':'d-flex flex-column'}) # align-items-stretch
		if is_editing:
			elt = html.DIV('UI_Source', **{'class':'alert alert-info', 'role':'alert'})
		self.obj = None
		UI_Component.__init__(self, elt, is_editing)
		self.is_editing = True
	def remove_child(self, child, fire_change_event):
		return child.clone()
	def clone(self):
		return UI_Source(self.config, self.is_editing)
	def get_json(self):
		return {'type':'UI_Source', 'config':self.config}
	# data
	def get_data(self, data_name):
		raise NotImplementedError()
	def set_config(self, config, edited):
		self.config = copy_config(config, self.is_editing)
	def set_data(self, data_name, data):
		for_layout = ('attr' in self.config) and ('for_layout' in self.config['attr']) and self.config['attr']['for_layout'] == 'true'
		self.elt.clear()
		for row in data['rows']:
			component_name, config_template, _ = row
			if config_template == '': continue # the config template has not been written
			config_template = JSON.parse(config_template)
			is_layout = ('tag' in config_template) and (config_template['tag'].startswith('#'))
			if for_layout != is_layout: continue
			self.elt <= html.DIV(html.SPAN(component_name, style={'margin':'2px'}, **{'class':'badge badge-pill badge-secondary'}))
			component = make_component(get_source_ui_json(config_template), True)
			self.elt <= component.elt
			component.mounted(self)

#imported UI_Editor

class UI_Editor(Custom_Component):
	def __init__(self, config, is_editing=False):
		elt = html.DIV(style={'padding':'5px', 'min-height':'700px'}, **{'class':'bg-light'})
		if is_editing:
			elt = html.DIV('UI_Editor', **{'class':'alert alert-info', 'role':'alert'})
		UI_Component.__init__(self, elt, is_editing)
		self.config = copy_config(config, is_editing)
		self.obj = None
		self.selected = None
		self.event_listener = None
		if not is_editing:
			self._set_component(None, True, False)
			self.edit_listener = self._edit_listener
		self.component_row = None
		self.val_column = 2
	def mounted(self, parent):
		self.parent = parent
		if self.is_editing:
			self.edit_listener = parent.edit_listener
		return self
	def _edit_listener(self, event_name, obj):
		if self.event_listener is not None:
			if event_name == 'selected':
				self.selected = obj
				self.event_listener('change', 'config')
			elif event_name == 'edited':
				self.event_listener('change', 'component')
	def get_data(self, data_name):
		if data_name == 'config':
			if self.selected is None: return None
			if self.selected.config is None: return None
			return self.selected.config # this violate that data is a table, but UI_Editor is not a public component
		elif data_name == 'component':
			if self.component_row is None: return None
			row = self.component_row['rows'][0]
			row[self.val_column] = JSON.stringify(self.component.get_json())
			return self.component_row
		else:
			raise AssertionError('Unknown data: ' + data_name)
	def set_data(self, data_name, data):
		if data_name == 'config':
			self.selected.set_config(data, False)
			if self.event_listener is not None:
				self.event_listener('change', 'component')
		elif data_name == 'component':
			if data is None:
				if self.component_row is None: return
				self.component_row = None
				self._set_component(None, True, False)
			else:
				self.component_row = data
				row = data['rows'][0]
				if row[self.val_column] == '': 
					self._set_component(None, True, True)
				else:
					component_config = row[self.val_column]
					component_config = JSON.parse(component_config)
					component = make_editing_ui(self, component_config)
					self._set_component(component, False, True)
		else:
			raise AssertionError('Unknown data: ' + data_name)	
	def _set_component(self, component, to_mount, placeholder_for_none):
		if component is None and placeholder_for_none:
			component = UI_Placehoder(True)
		self.component = component
		if self.component is None:
			self.elt.clear()
		if self.component is not None and to_mount:
			self.elt.clear()
			self.elt <= component.elt
			component.mounted(self)
		if self.selected is not None:
			self.selected = None
			if self.event_listener is not None:
				self.event_listener('change', 'config')
	def child_drop(self, child):
		if UI_Component.dragging is None: return
		dragging = UI_Component.dragging
		if dragging.parent is not None:
			dragging = dragging.parent.remove_child(dragging, False)
		self._set_component(dragging, True, False)
		if self.event_listener is not None:
			self.event_listener('change', 'component')
	def remove_child(self, child, fire_change_event):
		self._set_component(None, True, True)
		if fire_change_event and self.event_listener is not None:
			self.event_listener('change', 'component')
		return child
	def clone(self):
		return UI_Editor(self.config, self.is_editing)
	def get_json(self):
		return {'type':'UI_Editor', 'config':self.config}
	def set_config(self, config, edited):
		self.config = copy_config(config, self.is_editing)

def make_editing_ui(parent, ui_json):
	fix_ui_json(ui_json)
	def make_components(ui_json):
		obj = make_component(ui_json, True)
		obj_children = None
		if 'children' in ui_json and len(ui_json['children']) > 0: 
			obj_children = [make_components(child_ui_json) for child_ui_json in ui_json['children']]
		return obj, obj_children
	def set_children(obj, obj_children):
		if obj_children is None or len(obj_children) == 0: return
		children_objs = [obj2 for obj2, _ in obj_children]
		obj.set_children(children_objs)
		for obj2, obj_children2 in obj_children:
			set_children(obj2, obj_children2)
	obj, obj_children = make_components(ui_json)
	parent.elt.clear()
	parent.elt <= obj.elt
	obj.mounted(parent)
	set_children(obj, obj_children)
	return obj


