	
class _ui_elt_preview_helper:
	def __init__(self, component, data_hub):
		self.config = { 'data':{'config':'$config'}, 'init':'_ui_elt_preview_helper' }
		self.component = component
		self.data_hub = data_hub
		self.event_listener = None
	def set_data(self, data_name, data):
		self.data_hub.remove_component(self.component)
		self.component.set_config(data, False)
		self.data_hub.add_component(self.component)
		self.data_hub.onevent('', '', '')
	def get_data(self, data_name):
		return self.component.config
	def set_event_listener(self, event_listener):
		self.event_listener = event_listener

class ui_elt_preview_py:
	def __init__(self):
		self.elt = html.DIV(style={'margin':'10px'})
		self.event_listener = None
		self.helper = None
		self.config_edit_table = None
		self.component = None
		self.data_hub = None
	def use_example_data(self):
		wrap_in_card('预览', self.elt)
	def set_config(self, config):
		_set_config(self.elt, config)
		self.config = config
	def set_data(self, data_name, data):
		global user_info
		self.elt.clear()
		if data is None: return
		card_body = wrap_in_card('预览', self.elt)
		data_column = int(self.config['attr']['data_column'])
		config_template = data['rows'][0][data_column]
		if config_template == '': return
		config_template = JSON.parse(config_template)
		ui_json = get_source_ui_json(config_template)
		component = make_component(ui_json, False)
		config_edit_table = None
		if component.config is not None:
			component.config['__meta__'] = ui_json['config']['__meta__']
			component.use_example_data()
			config_template = "{\"name\":\"config_edit_table\",\"tag\":\"\",\"text\":\"\",\"init\":\"config_edit_table_obj_js\",\"files\":[\"ui/config_edit_table.js\"],\"data\":[\"data\", \"config\",\"page\"],\"ref\":[],\"events\":[],\"class\":{},\"attr\":{},\"style\":{}}"
			config_template = JSON.parse(config_template)
			config = get_source_ui_json(config_template)['config']
			config['data']['data'] = '@ui.names'
			config['data']['config'] = '$config'
			config['style']['margin'] = '10px'
			config_edit_table = Custom_Component(config, False)
			config_edit_table.set_data('page', {'rows':[['','测试']]})

		if self.data_hub is None:
			self.data_hub = DataHub(user_info[0])
		elif self.helper is not None:
			self.data_hub.remove_component(self.helper)
			self.data_hub.remove_component(self.config_edit_table)
			self.data_hub.remove_component(self.component)
		data_hub = self.data_hub
		flow_layout = FlowLayout(config={'style':{'margin':'0px'}}, is_editing=False, data_hub=data_hub)
		vertical_flow_layout = VerticalFlowLayout(config={'style':{'margin':'0px'}}, is_editing=False, data_hub=data_hub)
		card_body <= flow_layout.elt
		if config_edit_table is None:
			flow_layout.set_children([vertical_flow_layout])
		else:
			flow_layout.set_children([vertical_flow_layout, config_edit_table])
		vertical_flow_layout.set_children([component])
		helper = _ui_elt_preview_helper(component, data_hub)
		data_hub.add_component(helper)
		helper.event_listener('change', 'config')
		self.helper = helper
		self.config_edit_table = config_edit_table
		self.component = component
		self.data_hub.onevent('', '', '')

	def dispose(self):
		if self.data_hub is not None:
			self.data_hub.dispose()


