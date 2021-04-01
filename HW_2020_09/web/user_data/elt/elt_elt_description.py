from javascript import Date

class elt_elt_description_py:
	def __init__(self):
		self.elt = html.DIV()
	def use_example_data(self):
		def convert_datetime_to_timestamp(datetime):
			datum = Date.parse(datetime)
			assert datum == datum, '不是时间: '+datetime # not a NaN
			return datum / 1000		
		component_id = 'component_id'
		publisher_id = 'component_id'
		publish_date = convert_datetime_to_timestamp('2020/01/01')
		price = 1
		num_uses = 2
		config_template = ''
		description = 'This is a description'
		self.data = {'field_names':['component_id', 'publisher_id', 'publish_date', 'price', 'num_uses', 'config_template', 'description'],
			'field_types':['text', 'text', 'time', 'number', 'number', 'text', 'text'],
			'rows':[[component_id, publisher_id, publish_date, price, num_uses, config_template, description]]}
		self.set_data(None, self.data)
	def set_data(self, data_name, data):
		def convert_timestamp_to_datetime(unixtimestamp):
			date = Date.new(unixtimestamp*1000)
			year = str(date.getFullYear())
			month = ('0'+str(date.getMonth()+1))[-2:]
			day = ('0'+str(date.getDate()))[-2:]
			return year+'/'+month+'/'+day
		self.elt.clear()
		self.data = data
		if data is None: return
		component_id, publisher_id, publish_date, price, num_uses, config_template, description = self.data['rows'][0]
		card = html.DIV(style={'margin':'5px'}, **{'class':'card'})
		header = html.DIV(**{'class':'card-header'})
		publish_date = convert_timestamp_to_datetime(publish_date)
		price_text = '免费获取' if price == 0 else '%d元购买'%(price)
		global user_info
		client = user_info[0]
		if client == publisher_id:
			get_it = html.BUTTON('下架', style={'padding':'.4rem .4rem','line-height':'.6','border-radius':'.2rem'}, **{'class':'btn btn-danger btn-sm float-right align-middle'})
			def remove_from_store(ev):
				window.show_spinner_modal()
				self.event_listener('remove', component_id)
			def confirm_remove_from_store(ev):
				window.confirm_modal('请确认下您的架控件 "%s"'%component_id, remove_from_store)
			get_it.bind('click', confirm_remove_from_store)			
		else:
			get_it = html.BUTTON(price_text, style={'padding':'.4rem .4rem','line-height':'.6','border-radius':'.2rem'}, **{'class':'btn btn-primary btn-sm float-right align-middle'})
			def get_it_func(ev):
				window.show_spinner_modal()
				self.event_listener('buy', [publisher_id, component_id])
			get_it.bind('click', get_it_func)			
		header <= html.B(component_id, **{'class':'text-primary'}) + html.B('-', **{'class':'text-light'}) + \
			 	html.SMALL('by '+ html.B(publisher_id), **{'class':'text-info'}) + html.B('-', **{'class':'text-light'}) + \
			 	html.SMALL('used by '+ html.B(str(num_uses)), **{'class':'text-info'}) + html.B('-', **{'class':'text-light'}) + \
			 	html.SMALL(publish_date, **{'class':'text-secondary'}) + get_it
		card <= header
		card <= html.DIV(description, **{'class':'card-body'})
		self.elt <= card

