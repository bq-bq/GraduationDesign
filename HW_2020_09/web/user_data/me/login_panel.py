
# elt
# mounted(config)
# dispose()
# event_listener
# set_data(data_name, data)
# get_data(data_name)
# set_var(var_name, var_)
# get_var(var_name)

from browser import self as window

class login_panel_obj_py:
	def __init__(self):
		global user_info
		app_info = window.location.href.split('?')
		if len(app_info) == 1:
			app = 'me'
			app_secret = random_string(16)
			user_info = ['','',app,'']
		else:
			app_info = app_info[1].split('&')
			app_info = [info.split('=') for info in app_info]
			app_info = {info[0]:info[1] for info in app_info}
			user_info = app_info['user_info'].split('*')
			user_info = [window.decodeURI(info) for info in user_info]
			app, app_secret = user_info[2:]

		self.elt = html.DIV()

		card = html.DIV(style={'margin':'20px', 'width':'300px'}, **{'class':'card'})
		self.elt <= card
		card <= html.DIV('登录到应用 <b><span class=text-primary>%s<span></b>' % app.upper(), **{'class':'card-header'})
		form = html.FORM(**{'class':'card-body'})
		card <= form

		form_group1 = html.DIV(**{'class':'form-group'})
		form <= form_group1
		label1 = html.LABEL('用户名', **{'for':'user_name2'})
		form_group1 <= label1
		input1 = html.maketag('input')(**{'type':'text', 'class':'form-control', 'id':'user_name2', 'required':True, 'autocomplete':'user_name2', 'aria-describedby':'用户名'})
		form_group1 <= input1

		form_group2 = html.DIV(**{'class':'form-group'})
		form <= form_group2
		label2 = html.LABEL('密码', **{'for':'password2'})
		form_group2 <= label2
		input2 = html.maketag('input')(**{'type':'password', 'class':'form-control', 'id':'password2', 'required':True, 'autocomplete':'password2', 'aria-describedby':'密码'})
		form_group2 <= input2

		submit = html.BUTTON('登录', **{'type':'button', 'class':'btn btn-success'})
		form <= submit

		def on_login(data):
			if 'error' in data:
				window.error_toast(data['error'])
			else:
				user_info = [data['user'], data['session_code'], app, app_secret+data['app_secret']]
				window.location.href = '/%s?user_info=%s' % (app, '*'.join(user_info))
		def on_submit(ev):
			user_name = input1.value.strip()
			password = input2.value.strip()
			if app == '':
				window.error_toast('缺少应用名')
				return
			if user_name == '':
				window.error_toast('缺少用户名')
				return
			if password == '':
				window.error_toast('缺少密码')
				return
			input1.value = ''
			input2.value = ''
			data = {'user':user_name, 'pwd':password, 'app':app, 'app_secret':app_secret}
			send_ajax_request('login', 'login_with_pwd', data, on_login)
		submit.bind('click', on_submit)

		if user_info[0] == '': return

		card = html.DIV(style={'margin':'20px', 'width':'300px'}, **{'class':'card'})
		self.elt <= card
		card <= html.DIV('用户登退', **{'class':'card-header'})
		form = html.FORM(**{'class':'card-body'})
		card <= form

		submit = html.BUTTON('登退', **{'type':'button', 'class':'btn btn-danger'})
		form <= html.DIV('退出 <b><span class=text-primary>%s<span></b> 在所有设备上的登录' % user_info[0], **{'class':'form-group'})
		form <= submit

		def logout_callback(data):
			if 'error' in data:
				window.error_toast(data['error'])
			else:
				window.location.href = '/%s' % app
		def on_submit2(ev):
			send_ajax_request('login', 'logout', {'user_info':user_info}, logout_callback)
		submit.bind('click', on_submit2)


