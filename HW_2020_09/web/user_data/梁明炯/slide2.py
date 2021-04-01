#<div id="myCarousel" class="carousel slide">
#	<!-- 轮播（Carousel）指标 -->
#	<ol class="carousel-indicators">
#		<li data-target="#myCarousel" data-slide-to="0" class="active"></li>
#		<li data-target="#myCarousel" data-slide-to="1"></li>
##		<li data-target="#myCarousel" data-slide-to="2"></li>
#	</ol>   
#	<!-- 轮播（Carousel）项目 -->
##	<div class="carousel-inner">
#		<div class="item active">
#			<img src="/wp-content/uploads/2014/07/slide1.png" alt="First slide">
#		</div>
#		<div class="item">
#			<img src="/wp-content/uploads/2014/07/slide2.png" alt="Second slide">
#		</div>
#		<div class="item">
#			<img src="/wp-content/uploads/2014/07/slide3.png" alt="Third slide">
#		</div>
#	</div>
#	<!-- 轮播（Carousel）导航 -->
#	<a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
#		<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
#		<span class="sr-only">Previous</span>
#	</a>
#	<a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
#		<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
#		<span class="sr-only">Next</span>
#	</a>
#</div> 
	
	
class mingjiong_slide2_py_obj:

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
		self.my_data = {'field_names':['图片网址','网址'],\
			'field_types':['text','text'],\
			'rows':[['https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1588230440101&di=182dac8e549920745fe858e98f64803c&imgtype=0&src=http%3A%2F%2Fdpic.tiankong.com%2F5i%2Fhh%2FQJ8584996184.jpg','dropdowns2']]}
		self._update_component_UI() # 这个函数后面定义，用来根据设置更新控件
	
	
	def _update_component_UI(self):
		config = self.config
		data = self.my_data

		self.elt.clear() 
		if data is None or config is None: return
		slide = html.DIV(**{'class':'carousel slide', 'id':'myCarousel', 'data-ride':'carousel'})
		self.elt <= slide 
		ol = html.OL(**{'class':'carousel-indicators'})
		middiv = html.DIV(**{'class':'carousel-inner'})
		slide <=  ol
		slide <=  middiv
		aLeft = html.A(**{'class':'carousel-control-prev', 'href':'#myCarousel',  'role':'button', 'data-slide':'prev' })
		aRight = html.A(**{'class':'carousel-control-next', 'href':'#myCarousel',  'role':'button', 'data-slide':'next' })
		slide <=  aLeft
		slide <=  aRight

		aLeft<=html.SPAN(**{'class':'carousel-control-prev-icon', 'aria-hidden':'true'})
		aLeft<=html.SPAN(**{'class':'sr-only', 'text':'Previous'})
		aRight<=html.SPAN(**{'class':'carousel-control-next-icon', 'aria-hidden':'true'})
		aRight<=html.SPAN(**{'class':'sr-only', 'text':'Next'})

		def on_change(i, input):
			if self.event_listener is not None:
				self.event_listener('change', 'data1')
		for i in range(len(data['rows'])):
			temp = data['rows'][i][0]
			if i == 0:
				ol <= html.LI(**{'data-target':'#myCarousel', 'class':'active', 'data-slide-to':i})
				innerdiv = html.DIV(**{'class':'carousel-item active'})
			else:
				ol <= html.LI(**{'data-target':'#myCarousel', 'data-slide-to':i})
				innerdiv = html.DIV(**{'class':'carousel-item'})	
			innerdiv <= html.IMG(**{'src':temp, 'class':'d-block w-100', 'alt':'...'})
			middiv <= innerdiv