
from browser import self as window

class elt_store_pub_button:
	def __init__(self):
		self.elt = html.BUTTON('发布控件', **{'type':'button', 'class':'btn btn-info'})
		self.event_listener = None
		def onclick(ev):
			image = 'web/lib/icons/true/ios-cloud-upload.svg'
			inputs=[{'type':'text', 'id':'component-name', 'placeholder':'控件名'}, 
					{'type':'number', 'id':'component-price', 'placeholder':'价格'}]
			window.data_modal(image, None, inputs, '发布', publish_component)
		def publish_component(component_info):
			if self.event_listener is not None:
				window.show_spinner_modal()
				self.event_listener('publish_component', component_info)
		self.elt.bind('click', onclick)


