# this is a mini example for a easyweb component

class test_text_py:
	def __init__(self):
		self.elt = html.DIV()
		self.data = {'field_types': ['text'], 'field_names': ['name'], 'rows': [['Text']]}
		self.config = None

	def set_config(self, config):
		self.config = config
		self.__set_data()

	def set_data(self, data_name, data):
		self.data = data
		self.__set_data()

	def __get_attr(self, attr_name, default_value=None):
		if self.config is None: return default_value
		if 'attr' not in self.config: return default_value
		if attr_name not in self.config['attr']: return default_value
		return self.config['attr'][attr_name]

	def __set_data(self):
		self.elt.clear()
		tag = self.__get_attr('tag', 'span')
		if self.data is None or 'rows' not in self.data: return
		if len(self.data['rows']) == 0 or len(self.data['rows'][0]) == 0: return
		value = self.data['rows'][0][0]
		self.elt <= html.maketag(tag)(value)


