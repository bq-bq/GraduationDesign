
# elt
# mounted(config)
# dispose()
# event_listener
# set_data(data_name, data)
# get_data(data_name)
# set_var(var_name, var_)
# get_var(var_name)

from browser import self as window

class change_pwd_obj_py:
	def __init__(self):
		global user_info
		self.elt = html.DIV()
		card = html.DIV(style={'margin':'10px', 'width':'300px'}, **{'class':'card'})
		self.elt <= card
		card <= html.DIV('修改密码', **{'class':'card-header'})
		form = html.FORM(**{'class':'card-body'})
		card <= form

		form_group1 = html.DIV(**{'class':'form-group'})
		form <= form_group1
		label1 = html.LABEL('用户名', **{'for':'user_name'})
		form_group1 <= label1
		input1 = html.maketag('input')(**{'type':'text', 'disabled':'true', 'class':'form-control', 'id':'user_name', 'required':True, 'autocomplete':'username', 'aria-describedby':'用户名'})
		form_group1 <= input1
		input1.value = user_info[0]

		form_group2 = html.DIV(**{'class':'form-group'})
		form <= form_group2
		label2 = html.LABEL('旧密码', **{'for':'current-password'})
		form_group2 <= label2
		input2 = html.maketag('input')(**{'type':'password', 'class':'form-control', 'id':'current-password', 'required':True, 'autocomplete':'current-password', 'aria-describedby':'旧密码'})
		form_group2 <= input2

		form_group3 = html.DIV(**{'class':'form-group'})
		form <= form_group3
		label3 = html.LABEL('新密码', **{'for':'new-password'})
		form_group3 <= label3
		input3 = html.maketag('input')(**{'type':'password', 'class':'form-control', 'id':'new-password', 'required':True, 'autocomplete':'new-password', 'aria-describedby':'新密码'})
		form_group3 <= input3

		form_group4 = html.DIV(**{'class':'form-group'})
		form <= form_group4
		label4 = html.LABEL('新密码(确认)', **{'for':'new-password-2'})
		form_group4 <= label4
		input4 = html.maketag('input')(**{'type':'password', 'class':'form-control', 'id':'new-password-2', 'required':True, 'autocomplete':'new-password', 'aria-describedby':'新密码(确认)'})
		form_group4 <= input4

		submit = html.BUTTON('提交修改', **{'type':'button', 'class':'btn btn-primary'})
		form <= submit

		def on_pwd_updated(data):
			if 'error' in data:
				window.error_toast(data['error'])
			else:
				window.info_toast('密码已修改.')
		def on_submit(ev):
			user_name = input1.value.strip()
			current_password = input2.value.strip()
			new_password = input3.value.strip()
			new_password2 = input4.value.strip()
			if user_name == '':
				window.error_toast('缺少用户名')
				return
			if current_password == '':
				window.error_toast('缺少用旧密码')
				return
			if new_password == '':
				window.error_toast('缺少用新密码')
				return
			if new_password != new_password2:
				window.error_toast('两个新密码不相同')
				return
			input2.value = ''
			input3.value = ''
			input4.value = ''
			data = {'user_name':user_name, 'current_password':current_password,'new_password':new_password}
			send_ajax_request('login', 'change_pwd', data, on_pwd_updated)
		submit.bind('click', on_submit)

