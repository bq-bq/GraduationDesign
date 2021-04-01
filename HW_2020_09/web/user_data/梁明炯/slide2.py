#<div id="myCarousel" class="carousel slide">
#	<!-- �ֲ���Carousel��ָ�� -->
#	<ol class="carousel-indicators">
#		<li data-target="#myCarousel" data-slide-to="0" class="active"></li>
#		<li data-target="#myCarousel" data-slide-to="1"></li>
##		<li data-target="#myCarousel" data-slide-to="2"></li>
#	</ol>   
#	<!-- �ֲ���Carousel����Ŀ -->
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
#	<!-- �ֲ���Carousel������ -->
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

	# ����һ��py���󣬴���һ���ؼ�
	def __init__(self):
		# �ö�����Ҫ��һ����elt���ĵ��ڵ㣬��Ϊ�ÿؼ��ĸ��ڵ�
		self.elt = html.DIV()
		# �ö�����Ҫ��һ��config��Ա�����Դ�Ÿÿؼ���������Ϣ
		self.config = None
		# �ö�����Ҫ��һ��event_listener���������������������ҳ����
		# ���������������ҳ�������ؼ����͸ÿؼ����¼�
		self.event_listener = None
		# �����ǳ�Ա���Դ�Ÿÿؼ������ݣ���ÿ���ؼ��Լ�����
		self.my_data = None

	# ����ÿؼ����˱�����ݣ���ô��һ����Ϊdata_name�ı������
	# ���ı�Ϊdata��ʱ����ҳ��������set_data����
	def set_data(self, data_name, data): # data_name == 'data1'
		self.my_data = data # ����һ��dict��������field_names��field_types����list(str)��һ����rows��list(list(str))
		self._update_component_UI() # ����������涨�壬���������µ����ݸ��¿ؼ�

	# ����ÿؼ����˱�����ݣ���ô���ÿؼ�����self.event_listener
	# ����ҳ����������Ϊdata_name�ı�����ݵ�change�¼���
	# ��ҳ��������get_data������ȡ�ÿؼ��ĸñ������
	def get_data(self, data_name): # data_name == 'data1'
		return self.my_data

	# ��UIӦ��ʱ���ؼ������ÿ��Ա�UIӦ���Ҳ�����ñ���޸�
	# �ؼ������ñ��޸�ʱ���ú����ᱻ����
	def set_config(self, config):
		self.config = config # ����һ��dict�����������ֱ��attr,style,class��dict
		self._update_component_UI() # ����������涨�壬���������µ����ø��¿ؼ�

	# ĳЩ�ؼ���Ҫ�ڸ��ڵ�(self.elt)����ӵ���ҳ�������ȷ����
	# �ú�������self.elt����ӵ���ҳ�󱻵���
	# config ͬget_config�����Ĳ���
	# is_editing (True/False) ��ʾ��ǰ�ռ��Ƿ���UIӦ���б��༭
	# (������ؼ��ڱ��༭״̬����ʾ�ò�ͬ��ͨ���ڱ༭״̬�¿ؼ�����ռ��̫��Ŀռ�)
	# �ÿؼ�Ҳ���Ը����Լ���config��һ���޸���Ҫ����
	# if self.edit_listener is not None: self.edit_listener('edited', None)
	# ��֪ͨUIӦ��
	def mounted(self, config, is_editing, edit_listener):
		self.config = config
		self.edit_listener = edit_listener
		self._update_component_UI() # ����������涨�壬�����������ø��¿ؼ�

	# ���ؼ��ڱ��༭״̬ʱ���ú����ᱻ���ã������øÿؼ��ڱ��༭״̬ʱ������
	def use_example_data(self):
		self.my_data = {'field_names':['ͼƬ��ַ','��ַ'],\
			'field_types':['text','text'],\
			'rows':[['https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1588230440101&di=182dac8e549920745fe858e98f64803c&imgtype=0&src=http%3A%2F%2Fdpic.tiankong.com%2F5i%2Fhh%2FQJ8584996184.jpg','dropdowns2']]}
		self._update_component_UI() # ����������涨�壬�����������ø��¿ؼ�
	
	
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