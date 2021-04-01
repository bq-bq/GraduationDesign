
class tt_video_card_obj:
	def __init__(self):
		self.elt = html.DIV('12345')
		config = {'data': {}, 'vars': {}, 'events': {}, 'class': 'primary', 'attr': {'卡片视频': '', '卡片题目': '题目'}, 'style': {}}
		self.set_config(config)
	def set_config(self, config):
		color = 'light'
		card_title = '题目'
		card_video = None
		if 'class' in config:
			color = config['class']
		if 'attr' in config:
			attr = config['attr']
			if '卡片视频' in attr:
				card_video = attr['卡片视频']
			if '卡片题目' in attr:
				card_title = attr['卡片题目']
		card = html.DIV(**{'class':'alert alert-'+color, 'role':'alert'})
		card <= html.H4(card_title, **{'class':'alert-heading'})
		card <= html.HR()
		if card_video is None or card_video.strip() == '':
			card <= html.P('无视频')
		else:
			card <= html.maketag('video')(**{'src':card_video,'controls':'controls'})
		if 'style' in config:
			style = config['style']
			for key, val in style.items():
				card.style[key] = val
		self.elt.clear()
		self.elt <= card

