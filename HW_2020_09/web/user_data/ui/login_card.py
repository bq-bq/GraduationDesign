
def show_login(ev):
	from browser import self as window
	global user_info
	app_secret = random_string(16)
	window.location.href = '/me?user_info=%s&app_secret=%s' % ('*'.join(user_info), app_secret)

class ui_login_card_py:
	def __init__(self):
		self.elt = html.DIV()
		config = {'data': {}, 'vars': {}, 'events': {}, 'class': 'primary', 'attr': {'卡片文字': '设置页面', '卡片题目': '设置', '按钮文字': '登录'}, 'style': {}}
		self.set_config(config)
	def set_config(self, config):
		color = 'light'
		card_title = '登录卡片'
		card_text = []
		card_button = None
		if 'class' in config:
			color = config['class']
		if 'attr' in config:
			attr = config['attr']
			if '卡片文字' in attr:
				card_text = [t.strip() for t in attr['卡片文字'].split(';') if t.strip() != '']
			if '卡片题目' in attr:
				card_title = attr['卡片题目']
			if '按钮文字' in attr:
				card_button = attr['按钮文字']
		card = html.DIV(style={'margin':'10px', 'width':'100px'}, **{'class':'alert alert-'+color, 'role':'alert'})
		card <= html.H4(card_title, **{'class':'alert-heading'})
		if card_text is not None and len(card_text) > 0:
			card <= html.HR()
			for t in card_text:
				card <= html.P(t)
		if card_button is not None:
			info = {'class':'btn btn-'+color, 'href':'#'}
			card_button = html.A(card_button, **info)
			card_button.bind('click', show_login)
			card <= card_button
		if 'style' in config:
			style = config['style']
			for key, val in style.items():
				card.style[key] = val
		self.elt.clear()
		self.elt <= card

