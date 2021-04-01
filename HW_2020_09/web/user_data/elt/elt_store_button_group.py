
class elt_store_button_group:
	def __init__(self):
		self.elt = html.DIV(style={'margin':'0 auto'}, **{'class':'btn-group', 'role':'group'})
		text = html.INPUT(style={'width':'150px'}, **{'type':'search', 'class':'form-control', 'placeholder':'查找'})
		price = html.BUTTON('最低价格', style={'width':'100px'}, **{'type':'button', 'class':'btn btn-primary'})
		date = html.BUTTON('上架日期', style={'width':'100px'}, **{'type':'button', 'class':'btn btn-primary'})
		uses = html.BUTTON('使用次数', style={'width':'100px'}, **{'type':'button', 'class':'btn btn-primary'})
		self.elt <= text + price + date + uses
		cur_order = 'price'
		def onclick(ev):
			if ev.target == price:
				remove_class((date, uses), 'active')
				add_class(price, 'active')
				action('price')
			if ev.target == date:
				remove_class((price, uses), 'active')
				add_class(date, 'active')
				action('date')
			if ev.target == uses:
				remove_class((date, price), 'active')
				add_class(uses, 'active')
				action('uses')
			if ev.target == text:
				action(cur_order)
		def action(order):
			nonlocal cur_order
			cur_order = order
			if self.event_listener is not None:
				window.show_spinner_modal()
				self.event_listener('click_'+order, text.value)
		text.bind('blur', onclick)
		price.bind('click', onclick)
		date.bind('click', onclick)
		uses.bind('click', onclick)
		self.event_listener = None
