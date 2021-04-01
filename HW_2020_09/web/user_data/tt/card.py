
class tt_card_obj:
	def __init__(self):
		self.elt = html.DIV('12345')
		config = {'data': {}, 'vars': {}, 'events': {}, 'class': 'primary', 'attr': {'卡片文字': '设置页面', '卡片题目': '设置', '按钮文字': 'ME'}, 'style': {}}
		self.set_config(config)
	def set_config(self, config):
		color = 'light'
		card_title = '题目'
		card_text = []
		card_button = None
		card_link = None
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
			if '按钮链接' in attr:
				card_link = attr['按钮链接']
		card = html.DIV(**{'class':'alert alert-'+color, 'role':'alert'})
		card <= html.H4(card_title, **{'class':'alert-heading'})
		if card_text is not None and len(card_text) > 0:
			card <= html.HR()
			for t in card_text:
				card <= html.P(t)
		if card_button is not None:
			info = {'class':'btn btn-'+color, 'href':'#'}
			if card_link is not None:
				info['href'] = card_link
			card <= html.A(card_button, **info)
		if 'style' in config:
			style = config['style']
			for key, val in style.items():
				card.style[key] = val
		self.elt.clear()
		self.elt <= card

