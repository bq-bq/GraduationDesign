
# ����ؼ�������ʾһ�����ݿ���ĵ�һ��
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
# �������а������»ص����� set_data, get_data, get_config, mounted, use_example_data
# ����ص������е�ÿһ�����û�б�Ҫ�ǿ��Ժ��Բ�д��

class mingjiong_dropdowns2_py_obj:

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
		self.my_data = {'field_names':['����','��ַ'],\
			'field_types':['text','text'],\
			'rows':[['option1','option2']]}
		self._update_component_UI() # ����������涨�壬�����������ø��¿ؼ�

	def _update_component_UI(self):
		config = self.config
		data = self.my_data

		self.elt.clear() # ��ոÿؼ��Ľڵ�
		if data is None or config is None: return
		dropdown = html.DIV(**{'class':'dropdown'})
		self.elt <= dropdown # ���dropdown�ؼ�
		
		buttonClass = config['class'].strip()
		
		aa = html.A(**{'role':'button', 'class':f"btn {buttonClass} dropdown-toggle",'href':'#', 'data-toggle':'dropdown', 'id':'dropdownMenu1','aria-haspopup':'true', 'aria-expanded':'false'})
		aa.text='menu'
		dropdown <= aa

		innerdiv = html.DIV(**{'class':'dropdown-menu', 'aria-labelledby':'dropdownMenu1'})
		dropdown <= innerdiv


		def on_change(i, input):
			if self.event_listener is not None:
				self.event_listener('change', 'data1') # ֪ͨ��ҳ��Ϊ'data1'�����ݱ��޸���
		for i in range(len(data['rows'])):
			row = data['rows'][i]
			a = html.A(**{'class':'dropdown-item', 'href':row[0]})
			a.text = row[1]
			innerdiv <= a
		