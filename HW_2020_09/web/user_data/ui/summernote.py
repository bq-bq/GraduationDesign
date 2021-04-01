
from browser import self as window
jq = window.jQuery

def _summernote_obj_get_config(config):
	data_column = None
	if 'data_column' in config['attr']:
		data_column = int(config['attr']['data_column'])
	editable = False
	if 'editable' in config['attr']:
		editable = config['attr']['editable'] == 'True'
	margin = None
	if 'margin' in config['style']:
		margin = config['style']['margin']
	width = None
	if 'width' in config['style']:
		width = config['style']['width']
	return data_column, editable, margin, width

class summernote_obj_py:
	obj_count = 0
	def __init__(self):
		summernote_obj_py.obj_count += 1
		self.summernote_obj_id = 'summernote_obj_%d' % summernote_obj_py.obj_count
		self.elt = html.DIV()
		self.edit_listener = None
		self.is_editing = None
		self.data = None
		self.config = None

	def set_config(self, config):
		if self.config is None:
			self.config = config
			return
		config['attr']['innerHTML'] = self.config['attr']['innerHTML']
		self.config = config
		self._set_data(self.is_editing, False)

	def mounted(self, config, is_editing, edit_listener):
		self.config = config
		self.is_editing = is_editing
		self.edit_listener = edit_listener
		if not is_editing:
			if 'attr' not in config or 'innerHTML' not in config['attr'] or config['attr']['innerHTML'].strip() == '': return
		self._set_data(is_editing, False)

	def _set_data(self, is_editing, use_data):
		data_column, editable, margin, width = _summernote_obj_get_config(self.config)
		config = self.config
		self.elt.clear()
		if use_data:
			if self.data is None: return
			if 'rows' not in self.data:
				window.error_toast('%s 不是数据'%data_name);
				return
			rows = self.data['rows']
			innerHTML = rows[0][data_column]
		else:
			if 'innerHTML' not in config['attr']:
				config['attr']['innerHTML'] = ''
			innerHTML = config['attr']['innerHTML']
		editor = html.DIV(**{'id':self.summernote_obj_id})
		self.elt <= editor
		if margin is not None:
			self.elt.style['margin'] = margin
		if width is not None:
			self.elt.style['width'] = width

		self.elt.children[0].innerHTML = innerHTML
		if is_editing:
			def onBlur(ev):
				if 'innerHTML' not in config['attr'] or config['attr']['innerHTML'] != ev.target.innerHTML:
					config['attr']['innerHTML'] = ev.target.innerHTML
					if self.edit_listener is not None:
						self.edit_listener('edited', None)
			jq('#'+self.summernote_obj_id).summernote({'callbacks':{'onBlur':onBlur}})
		else:
			if editable:
				def onBlur(ev):
					if rows[0][data_column] != ev.target.innerHTML:
						rows[0][data_column] = ev.target.innerHTML
						if self.event_listener is not None:
							self.event_listener('change', 'data')
				jq('#'+self.summernote_obj_id).summernote({'callbacks':{'onBlur':onBlur}})


	def set_data(self, data_name, data):
		self.data = data
		self._set_data(False, True)

	def get_data(self, data_name):
		return self.data

		

