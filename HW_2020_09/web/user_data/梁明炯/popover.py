
#<button type="button" class="btn btn-secondary" data-container="body" data-toggle="popover" data-placement="top" data-content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.">
#  Popover on top
#</button>
# 本例子中包含以下回调函数 set_data, get_data, get_config, mounted, use_example_data
# 这个回调函数中的每一个如果没有必要是可以忽略不写的

class mingjiong_popover2_py_obj:

	# 创建一个py对象，代表一个控件
	def __init__(self):
		# 该对象需要有一个叫elt的文档节点，作为该控件的根节点
		self.elt = html.DIV()
		# 该对象需要有一个config成员，用以存放该控件的设置信息
		self.config = {'class': 'btn btn-secondary', 'attr': {'按钮文字': '按钮', '弹出方向': '向上', '弹出文字': '这是个实例'}, 'style': {}}
		#self.set_config(self.config)

	def set_config(self, config):
		self.config = config # 这是一个dict，包含三个分别叫attr,style,class的dict
		self._update_component_UI() # 这个函数后面定义，用来根据新的设置更新控件

	def _update_component_UI(self):
		config = self.config

		self.elt.clear() # 清空该控件的节点
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