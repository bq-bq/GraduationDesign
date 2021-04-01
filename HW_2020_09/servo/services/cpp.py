
from ..core.db import context, query, time_to_text
from . import cpp_tools
import time

def on_cpp_test_cpp(app, client, action, 当前题目1, 运行结果, **kwargs):
	assert app in ('c', 'cpp'), '这个事件响应程序只能由应用 cpp 使用'
	题目名,问题,主程序,答案程序,随机输入产生程序,开始时间,截止时间 = 当前题目1.get_rows()[0]
	try:
		res = cpp_tools.run_source(client, 主程序, [答案程序], 随机输入产生程序)
		input_text, output_text = res
		res = '# 输入\n' + input_text + '\n\n# 输出\n' + output_text
	except AssertionError as ex:
		res = str(ex)
	if len(运行结果) == 0:
		运行结果 ** res
	else:
		运行结果 << res
	

def on_cpp_student_list(app, client, action, 题目, 答案, **kwargs):
	assert app in ('c', 'cpp'), '这个事件响应程序只能由应用 cpp 使用'
	assert client is not None, '请登录'
	rows = []
	res = {'field_names': ['题目名', '问题', '主程序', '答案', '评语', '开始时间', '截止时间', '分数', '提交时间'],
			'field_types': ['text', 'text', 'text', 'text', 'text', 'time', 'time', 'number', 'time'], 
			'rows': rows}
	cur_time = time.time()
	答案 = query(select=答案, where=答案.用户名 == client)
	for 题目名,问题,主程序,答案程序,随机输入产生程序,开始时间,截止时间 in 题目.get_rows():
		if 开始时间 < cur_time < 截止时间:
			row = [题目名,问题,主程序,'','',开始时间,截止时间,0,'']
			ans = query(select=[答案.答案, 答案.评语, 答案.分数, 答案.提交时间], where=答案.题目名==题目名)
			if len(ans) > 0:
				ans = ans.get_rows()
				row[3], row[4], row[7], row[8] = ans[0]
			rows.append(row)
	return res

def on_cpp_answer_list(app, client, action, 题目, 答案, **kwargs):
	assert app in ('c', 'cpp'), '这个事件响应程序只能由应用 cpp 使用'
	assert client is not None, '请登录'
	rows = []
	res = {'field_names': ['题目名', '主程序', '答案'],
			'field_types': ['text', 'text', 'text'], 
			'rows': rows}
	if app != client:
		答案 = query(select=答案, where=答案.用户名 == client)
		for 题目名,问题,主程序,答案程序,随机输入产生程序,开始时间,截止时间 in 题目.get_rows():
			row = [题目名,主程序,'']
			ans = query(select=[答案.答案, 答案.分数], where=答案.题目名==题目名)
			if len(ans) > 0:
				ans = ans.get_rows()
				cpp_answer, 分数 = ans[0]
				row[0] = '<h3>%s - %d分</h3>' % (row[0], 分数) 
				row[2] = cpp_answer
				rows.append(row)
	else:
		title = []
		main = {}
		for 题目名,问题,主程序,答案程序,随机输入产生程序,开始时间,截止时间 in 题目.get_rows():
			title.append(题目名)
			main[题目名] = 主程序
		clients_folder = os.path.join('user_db', app, 'clients')
		clients = [c for c in os.listdir(clients_folder) if os.path.isdir(os.path.join(clients_folder, c))]
		for 用户名 in clients:
			with context('cpp', 用户名) as c:
				答案 = c.tables['答案']
				cpp_answer = query(select=[答案.题目名, 答案.答案, 答案.分数], where=答案.用户名 == 用户名)
				for 题目名, 答案, 分数 in cpp_answer.get_rows():
					if 题目名 not in main: continue
					rows.append(['<h3>%s - %s - %d分</h3>'%(用户名,题目名,分数), None, 答案])
	return res

def on_cpp_answer_sumbit(app, client, action, 题目, 答案, 当前题目2, **kwargs):
	assert app in ('c', 'cpp'), '这个事件响应程序只能由应用 cpp 使用'
	assert client is not None, '请登录'
	cur_time = time.time()
	题目名,问题,主程序,新答案,评语,开始时间,截止时间,分数,提交时间 = 当前题目2.get_rows()[0]
	题目 = query(select=题目, where=题目.题目名==题目名).get_rows()
	assert len(题目) > 0, '不存在题目: '+题目名
	题目名,问题,主程序,答案程序,随机输入产生程序,开始时间,截止时间 = 题目[0]
	assert 开始时间<cur_time, '还未到开始时间: '+time_to_text(开始时间)
	assert 截止时间>cur_time, '已超过截止时间: '+time_to_text(截止时间)
	try:
		res = cpp_tools.run_source(client, 主程序, [答案程序,新答案], 随机输入产生程序)
		input_text, output_text1, output_text2 = res
		score = 0
		output_lines1 = output_text1.strip().split('\n')
		output_lines2 = output_text2.strip().split('\n')
		if len(output_lines1) == len(output_lines2):
			score += 1
		for line1, line2 in zip(output_lines1, output_lines2):
			if line1.strip() == line2.strip(): score += 1
		score = score / (len(output_lines1) + 1)
		if score == 1:
			comment = '# 答案正确'
		else:
			comment = '# 答案不正确\n\n'+'# 随机输入:\n'+input_text+'\n\n# 参考答案:\n'+output_text1+'\n\n# 我的答案:\n'+output_text2
	except AssertionError as ex:
		comment = str(ex)
		score = 0
	score = int(score * 100)
	答案1 = query(答案, where=(答案.题目名==题目名) & (答案.用户名==client))
	if len(答案1) > 0:
		题目名,用户名,旧答案,提交时间,分数,评语 = 答案1.get_rows()[0]
		if score >= 分数:
			分数 = score
			提交时间 = cur_time
		答案1 << [题目名,用户名,新答案,提交时间,分数,comment]
	else:
		答案 ** [题目名,client,新答案,cur_time,score,comment]
