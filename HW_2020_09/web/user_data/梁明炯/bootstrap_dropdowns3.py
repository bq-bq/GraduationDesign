
# 这个控件用来显示一个数据库表格的第一行
#<div class="dropdown">
 # <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
  #  Dropdown link
  #</a>

  #<div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
   # <a class="dropdown-item" href="#">Action</a>
    #<a class="dropdown-item" href="#">Another action</a>
    #<a class="dropdown-item" href="#">Something else here</a>
  #</div>
#</div>
# 本例子中包含以下回调函数 set_data, get_data, get_config, mounted, use_example_data
# 这个回调函数中的每一个如果没有必要是可以忽略不写的

class mingjiong_dropdowns2_py_obj:

	# 创建一个py对象，代表一个控件
	def __init__(self):
		# 该对象需要有一个叫elt的文档节点，作为该控件的根节点
		self.elt = html.DIV()
		# 该对象需要有一个config成员，用以存放该控件的设置信息
		self.config = None
		# 该对象需要有一个event_listener函数，这个函数将会有网页设置
		# 这个函数用以向网页和其它控件发送该控件的事件
		self.event_listener = None
		# 以下是成员用以存放该控件的数据，由每个控件自己定义
		self.my_data = None

	# 如果该控件绑定了表格数据，那么当一个名为data_name的表格数据
	# 被改变为data的时候，网页会调用这个set_data函数
	def set_data(self, data_name, data): # data_name == 'data1'
		self.my_data = data # 这是一个dict，包含叫field_names和field_types两个list(str)和一个叫rows的list(list(str))
		self._update_component_UI() # 这个函数后面定义，用来根据新的数据更新控件

	# 如果该控件绑定了表格数据，那么当该控件调用self.event_listener
	# 向网页发送了名字为data_name的表格数据的change事件后，
	# 网页会调用这个get_data函数获取该控件的该表格数据
	def get_data(self, data_name): # data_name == 'data1'
		return self.my_data

	# 在UI应用时，控件的设置可以被UI应用右侧的设置表格修改
	# 控件的设置被修改时，该函数会被调用
	def set_config(self, config):
		self.config = config # 这是一个dict，包含三个分别叫attr,style,class的dict
		self._update_component_UI() # 这个函数后面定义，用来根据新的设置更新控件

	# 某些控件需要在根节点(self.elt)被添加到网页后才能正确构建
	# 该函数会在self.elt被添加到网页后被调用
	# config 同get_config函数的参数
	# is_editing (True/False) 表示当前空间是否在UI应用中被编辑
	# (这允许控件在被编辑状态被显示得不同，通常在编辑状态下控件不易占用太大的空间)
	# 该控件也可以更改自己的config，一但修改需要调用
	# if self.edit_listener is not None: self.edit_listener('edited', None)
	# 以通知UI应用
	def mounted(self, config, is_editing, edit_listener):
		self.config = config
		self.edit_listener = edit_listener
		self._update_component_UI() # 这个函数后面定义，用来根据设置更新控件

	# 当控件在被编辑状态时，该函数会被调用，以设置该控件在被编辑状态时的数据
	def use_example_data(self):
		self.my_data = {'field_names':['文字','网址'],\
			'field_types':['text','text'],\
			'rows':[['option1','option2']]}
		self._update_component_UI() # 这个函数后面定义，用来根据设置更新控件

	def _update_component_UI(self):
		config = self.config
		data = self.my_data

		self.elt.clear() # 清空该控件的节点
		if data is None or config is None: return
		dropdown = html.DIV(**{'class':'dropdown'})
		self.elt <= dropdown # 添加dropdown控件
		
		buttonClass = config['class'].strip()
		
		aa = html.A(**{'role':'button', 'class':f"btn {buttonClass} dropdown-toggle",'href':'#', 'data-toggle':'dropdown', 'id':'dropdownMenu1','aria-haspopup':'true', 'aria-expanded':'false'})
		aa.text='menu'
		dropdown <= aa

		innerdiv = html.DIV(**{'class':'dropdown-menu', 'aria-labelledby':'dropdownMenu1'})
		dropdown <= innerdiv


		def on_change(i, input):
			if self.event_listener is not None:
				self.event_listener('change', 'data1') # 通知网页名为'data1'的数据被修改了
		for i in range(len(data['rows'])):
			row = data['rows'][i]
			a = html.A(**{'class':'dropdown-item', 'href':row[0]})
			a.text = row[1]
			innerdiv <= a
		