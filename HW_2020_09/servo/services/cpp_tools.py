
import os, sys, tempfile, signal, time
from subprocess import Popen, PIPE, CalledProcessError
from threading import Timer

def decode_text(text, info):
	if text is None: return None
	codes = ['utf-8', 'windows-1252', 'ISO-8859-1', 'GB2312']
	for code in codes:
		try:
			return text.decode(code)
		except:
			pass
	assert False, '%s Input file cannot be decoded, please try to use a different browser.' % info

def run_cmd(cmd, files, temp_dir, info, timeout=1, shell=True):
	for name in files:
		if files[name] is not None:
			with open(os.path.join(temp_dir, name), 'w') as f:
				f.write(files[name])
	try:
		proc = Popen(cmd, cwd=temp_dir, stdout=PIPE, stderr=PIPE, shell=shell, preexec_fn=os.setsid)
		is_timeout = False
		def kill_proc(proc):
			nonlocal is_timeout
			os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
			is_timeout = True
		timer = Timer(timeout, kill_proc, (proc,))
		try:
			timer.start()
			output, error = proc.communicate() # stdout, stderr
			output = decode_text(output, 'The stdout output of ' + info)
			error = decode_text(error, 'The stderr output of ' + info)
			assert error is None or error.strip() == '', error
			assert not is_timeout, '%s timeouts (%d seconds)' % (info, timeout)
			return output
		finally:
			timer.cancel()
	except CalledProcessError:
		assert False, 'The procedure returns nonzero.'
	# except Exception as ex:
	# 	return str(ex)
	finally:
		to_remove = []
		for name in files:
			file_path = os.path.join(temp_dir, name)
			if os.path.isfile(file_path):
				to_remove.append(file_path)
			else:
				print('No such file to delete: ' + file_path)
		if len(to_remove) > 0:
			time.sleep(.1)
			for file_path in to_remove:
				os.unlink(file_path)

def find_included(source):
	included = set()
	for line in source.split('\n'):
		line = line.strip()
		if line.startswith('#include'):
			line = line[8:].strip()
			included.add(line)
	return included

def get_compiler(main_source):
	included = find_included(main_source)
	if '"source.cpp"' in included:
		is_cpp = True
	elif '"source.c"' in included:
		is_cpp = False
	else:
		assert False, '主程序必须包含 "source.cpp" 或 "source.c"'
	assert '"main.cpp"' not in included and '"main.c"' not in included, "主程序不能包含自己"
	if is_cpp:
		return 'g++ -std=c++11 -O1 -g -fno-omit-frame-pointer -fsanitize=address -fPIE'
	else:
		return 'gcc -g -fno-omit-frame-pointer -fsanitize=address -fPIE'
		# return 'gcc -O1 -g -fno-omit-frame-pointer -fsanitize=address -fPIE'

cpp_headers_allowed = ['<iostream>', '<iomanip>', '<string>', '<vector>', '<sstream>', '<stdexcept>', 
				'<stack>', '<queue>', '<cstring>', '<cmath>']

c_headers_allowed = ['<stdio.h>', '<string.h>', '<cmath.h>']

def check_headers(sources, headers):
	headers = set(headers)
	for source in sources:
		included = find_included(source)
		included = included - headers
		assert len(included) == 0, '不允许使用的头文件: ' + ' '.join(included)

def run_source(client, main_source, cpp_sources, input_source):
	if sys.platform == 'darwin':
		return run_source_mac(client, main_source, cpp_sources, input_source)
	elif sys.platform == 'linux':
		return run_source_linux(client, main_source, cpp_sources, input_source)
	else:
		raise f'Unsupported OS: {sys.platform}'

# 为每个用户创建一个linux的普通账号，使得运行的程序互不影响。
# 其中，需要以root身份运行useradd和runuser。
# -O1 优化
# -g enables use of extra debugging information
# To use MSan, compile and link your program with -fsanitize=memory -fPIE -pie
# -fno-omit-frame-pointer   To get any stack traces
# ASAN_OPTIONS=detect_leaks=1  LeakSanitizer on x86_64 OS X
def run_source_linux(client, main_source, cpp_sources, input_source):
	compiler = get_compiler(main_source)
	is_cpp = (compiler[:3] == 'g++')
	check_headers(cpp_sources, (cpp_headers_allowed if is_cpp else c_headers_allowed))
	extention = ('.cpp' if is_cpp else '.c')
	linux_user = 'cpp_test'
	user_cpp_cwd = '/home'
	user_cpp_cwd = os.path.join(user_cpp_cwd, linux_user)
	if not os.path.isdir(user_cpp_cwd):
		os.system(f'useradd -d /home/{linux_user} -m {linux_user}')
	cpp_cwd = os.path.join(user_cpp_cwd, client)
	if not os.path.isdir(cpp_cwd):
		os.mkdir(cpp_cwd)
	input_text = ''
	if input_source is not None and input_source.strip() != '':
		cmd = ['python3 input.py']
		files = { 'input.py': input_source }
		input_text = run_cmd(cmd, files, cpp_cwd, 'Python', 5)
	res = [input_text]
	for cpp_source in cpp_sources:
		cmd = [f'{compiler} main{extention} -o main.out']
		files = { f'main{extention}': main_source, f'source{extention}': cpp_source }
		# print '正在编译'
		output = run_cmd(cmd, files, cpp_cwd, 'C/C++ compiler', 3)
		assert output.strip() == '', output
		cmd = ['runuser', '-l', linux_user, '-c', 'cd %s ; ulimit -t 2; ulimit -s 2048 ; ASAN_OPTIONS=detect_leaks=1 ./main.out < input.txt' % cpp_cwd]
		files = { 'input.txt': input_text, 'main.out': None }
		# print '正在运行'
		output = run_cmd(cmd, files, cpp_cwd, 'C/C++ program', 3, False)
		if len(output) > 10*1024:
			output = output[:10*1024]+' ...'
		res.append(output)
	os.rmdir(cpp_cwd)
	return res

def run_source_mac(client, main_source, cpp_sources, input_source):
	compiler = get_compiler(main_source)
	is_cpp = (compiler[:3] == 'g++')
	check_headers(cpp_sources, (cpp_headers_allowed if is_cpp else c_headers_allowed))
	extention = ('.cpp' if is_cpp else '.c')
	cpp_cwd_root = '_cpp_test'
	if not os.path.isdir(cpp_cwd_root):
		os.mkdir(cpp_cwd_root)
	with tempfile.TemporaryDirectory(dir=cpp_cwd_root) as cpp_cwd:
		try:
			input_text = ''
			if input_source is not None and input_source.strip() != '':
				cmd = ['python3 input.py']
				files = { 'input.py': input_source }
				input_text = run_cmd(cmd, files, cpp_cwd, 'Python', 5)
			res = [input_text]
			for cpp_source in cpp_sources:
				cmd = [f'{compiler} main{extention} -o main.out']
				files = { f'main{extention}': main_source, f'source{extention}': cpp_source }
				# print '正在编译'
				output = run_cmd(cmd, files, cpp_cwd, 'C/C++ compiler', 5)
				assert output.strip() == '', output
				if input_text.strip() != '':
					cmd = ['./main.out < input.txt']
					files = { 'input.txt': input_text, 'main.out': None }
				else:
					cmd = ['./main.out']
					files = { 'main.out': None }
				# print '正在运行'
				output = run_cmd(cmd, files, cpp_cwd, 'C/C++ program', 3)
				if len(output) > 10*1024:
					output = output[:10*1024]+' ...'
				res.append(output)
			return res
		finally:
			pass
		# for file in os.listdir(cpp_cwd):
		# 	print('removing file: ' + file)
		# 	os.unlink(os.path.join(cpp_cwd, file))
		# os.rmdir(cpp_cwd)



