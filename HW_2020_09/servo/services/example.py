
from ..core.db import query

def on_female_student(app, client, action, student, **kwargs):
	assert app == 'test', '这个事件响应程序只能由应用 \'test\' 使用'
	return query(select=[student.first_name, student.last_name], where=student.sex == 'Female')

def on_male_student(app, client, action, student, **kwargs):
	assert app == 'test', '这个事件响应程序只能由应用 \'test\' 使用'
	return query(select=[student.first_name, student.last_name], where=student.sex == 'Male')

