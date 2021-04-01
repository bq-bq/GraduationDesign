
#<button type="button" class="btn btn-secondary" data-container="body" data-toggle="popover" data-placement="top" data-content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.">
#  Popover on top
#</button>
# �������а������»ص����� set_data, get_data, get_config, mounted, use_example_data
# ����ص������е�ÿһ�����û�б�Ҫ�ǿ��Ժ��Բ�д��

class mingjiong_popover2_py_obj:

	# ����һ��py���󣬴���һ���ؼ�
	def __init__(self):
		# �ö�����Ҫ��һ����elt���ĵ��ڵ㣬��Ϊ�ÿؼ��ĸ��ڵ�
		self.elt = html.DIV()
		# �ö�����Ҫ��һ��config��Ա�����Դ�Ÿÿؼ���������Ϣ
		self.config = {'class': 'btn btn-secondary', 'attr': {'��ť����': '��ť', '��������': '����', '��������': '���Ǹ�ʵ��'}, 'style': {}}
		#self.set_config(self.config)

	def set_config(self, config):
		self.config = config # ����һ��dict�����������ֱ��attr,style,class��dict
		self._update_component_UI() # ����������涨�壬���������µ����ø��¿ؼ�

	def _update_component_UI(self):
		config = self.config

		self.elt.clear() # ��ոÿؼ��Ľڵ�
		if config is None: return

		buttonContent = 'button'
		popPlacement = 'top'
		popContent = 'popContent is not set'
		buttonClass = 'btn-secondary'


		if 'attr' in config:
			attr = config['attr']
			if 'buttonContent' in attr:
				buttonContent =  attr['buttonContent']
			if 'popPlacement' in attr:
				popPlacement = attr['popPlacement']
			if 'popContent' in attr:
				popContent = attr['popContent']

		if 'class' in config:
			buttonClass = config['class'].strip()

		popover = html.BUTTON(**{'id':'myButton', 'type':'button', 'class':f'btn {buttonClass}', 'data-container':'body', 'data-toggle':'popover', 'data-placement':f'{popPlacement}', 'data-content':f'{popContent}'})
		popover.text = buttonContent
		self.elt <= popover