
from browser import self as window

def _codemirror_from_textarea(textArea, editable, onSave, source_type):
	def on_save(ev):
		if onSave is not None: onSave()
	source_type = source_type.lower()
	config = {
		'lineNumbers': True,
		'lineWrapping': True,
		 # 'viewportMargin': 'Infinity',
		'tabSize': 4,
		'indentUnit': 4,
		'indentWithTabs': True,
		'matchBrackets': True,
		'autoCloseBrackets': True,
		'theme': ('blackboard' if editable else 'default'),
		'readOnly': not editable,
		'showCursorWhenSelecting': True,
		'keyMap': 'sublime',
		'extraKeys': {
			'Ctrl-S': on_save,
			'Cmd-S': on_save,
		},
	}
	if source_type == 'py':
		config['mode'] = {'name':'python', 'version':3, 'singleLineStringErrors':False}
	return window.CodeMirror.fromTextArea(textArea, config)


class pro_code_py:
	def __init__(self):
		self.type_name = 'pro_code'
		self.elt = html.DIV()
		self.event_listener = None
		self.config = None
		self.data = None
		self.editor = None
		self.file_name = None
	def use_example_data(self):
		source = "print('Hello')"
		self.config = {'attr':{'title':'编辑器'}}
		self.data = {'field_names': ['file_name', 'file_content'],
					'field_types': ['text', 'text'], 'rows':[['test.py',source]]}
		self._set_data()
	def get_data(self, data_name):
		return self.data
	def set_data(self, data_name, data):
		self.data = data
		self._set_data()
	def set_config(self, config):
		self.config = config
		self._set_data(True)
	def dispose(self):
		if self.editor is not None:
			self.editor.toTextArea()
			self.editor = None
	def _set_data(self, force_udpate=False):
		if self.data is None:
			self.elt.clear()
			return
		file_name, file_content = None, None
		if 'rows' in self.data and len(self.data['rows']) > 0:
			file_name, file_content = self.data['rows'][0]
		if self.editor is not None:
			cur_file_content = self.editor.getValue()
			if not force_udpate and self.file_name == file_name and file_content == cur_file_content: return
			self.dispose()
		self.elt.clear()
		self.file_name = file_name
		if file_content is None: return
		style = {}
		if 'style' in self.config:
			if 'margin' in self.config['style']:
				style['margin'] = self.config['style']['margin']
			if 'width' in self.config['style']:
				style['width'] = self.config['style']['width']
		if 'title' in self.config['attr']:
			card = html.DIV(style=style, **{'class':'card'})
			self.elt <= card
			card <= html.DIV(self.config['attr']['title'], **{'class':'card-header'})
			form = html.DIV(**{'class':'card-body'})
			card <= form
		else:
			# form = html.DIV(**{'class':'card-body'})
			form = html.DIV(style=style)
			self.elt <= form
		text_area = html.maketag('textarea')()
		form <= text_area
		editable = ('editable' not in self.config['attr'] or self.config['attr']['editable'] == 'True')
		def onSave():
			nonlocal editable
			if not editable: return
			value = self.editor.getValue()
			if value == self.data['rows'][0][1]: return
			self.data['rows'][0][1] = value
			if self.event_listener is not None:
				self.event_listener('change', 'data')
		file_extention = file_name.split('.')[-1]
		self.editor = _codemirror_from_textarea(text_area, editable, onSave, file_extention)
		self.editor.setValue(file_content)
		save_button = ('save_button' not in self.config['attr'] or self.config['attr']['save_button'] == 'True')
		if editable:
			if save_button:
				save_button = html.BUTTON('保存', style={'margin':'10px 0px 0px 0px'}, **{'class':'btn btn-primary'})
				form <= save_button
				save_button.bind('click', onSave)
			else:
				self.editor.on('blur', lambda editor, change: onSave())
