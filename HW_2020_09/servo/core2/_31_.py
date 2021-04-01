import os, json, io
from .db import context
from .. import lib
# _31_ 读取服务器主页信息
def _479_(_478_):
	_551_ = None
	with context(app='me', client=_478_) as _136_:
		if _136_._227_('settings'):
			_551_ = _136_.read('settings')
	if _551_ is not None:
		_551_ = _551_['rows']
		if len(_551_) == 0:
			_551_ = None
		else:
			_551_ = _551_[0]
	if _551_ is None:
		_482_, _555_, _488_ = _478_, '', ''
	else:
		_482_, _555_, _488_ = _551_
		if _482_.strip() == '': _482_ = _478_
		if _555_.strip() == '': _555_ = 'journal'
	return _482_, _555_, _488_

def _477_(_478_, _482_, _555_):
	_518_ = lib._29_._244_('web', 'index_lite.html')
	if _555_ not in ('', 'Default'):
		_536_ = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css">'
		_535_ = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/%s/bootstrap.min.css">' % _555_.lower()
	with open(_4_._813_, 'w') as _817_:
		with open(_518_,encoding='utf-8') as _815_:
			for _525_ in _815_:
				_525_ = _525_.replace("<title id='title'></title>", "<title id='title'>%s</title>" % _478_)
				_525_ = _525_.replace('<b class="navbar-brand" href="#" id=brand></b>', '<b class="navbar-brand" href="#" id=brand>%s</b>' % _482_)
				if _555_ not in ('', 'Default'):
					_525_ = _525_.replace(_536_, _535_)
				if _525_[-1] != '\n':
					_817_.write(_525_ + '\n')
				else:
					_817_.write(_525_)
	return True


class _4_:
	_813_ = 'web/__temp__.html'

	def __init__(_342_, _6_, **_550_):
		_342_._6_ = _6_
		_342_._550_ = _550_
		for _, _30_ in _550_.items():
			_30_._550_ = _550_

	def _443_(_342_, _461_):
		try:
			return _514_(_461_, _342_._550_)
		except AssertionError as _496_:
			return _816_(_496_, True)
		except Exception as _496_:
			print('Internal error (%s)' % type(_496_).__name__)
			return _816_(_496_, True)

	def _446_(_342_, _478_, _459_):
		def _818_(_18_):
			with open(_4_._813_, 'w') as _15_:
				_15_.write(_18_)
		def _543_(_32_, _445_):
			_18_ = "<html><head><meta http-equiv=\"Refresh\" content=\"0; url=//%s/%s\" /></head><body></body></html>" % (_32_, _445_)
			_818_(_18_)
			return True
		try:
			#assert 'root_server' in _342_._6_, '缺少运行必须的参数 root_server'
			if 'root_server' in _342_._6_:
				_547_ = _342_._6_['root_server']
			else:
				_547_ = 'localhost'
			if not lib._29_._240_(lib._29_._244_('user_db', 'ui', 'clients', _478_)):
				if _478_ == 'me' and 'user_info' in _459_:
					_565_ = _459_['user_info'].split('*')
					_565_ = {'user':_565_[0], 'session_code':_565_[1], 'app':_565_[2], 'app_secret':_565_[3]}
					_342_._550_['login'].logout(user_info=_565_) # logout on sub-server
					_478_ += '?user_info=%s' % _459_['user_info']
				return _543_(_547_, _478_)
			_482_, _555_, _488_ = _479_(_478_)
			return _477_(_478_, _482_, _555_)
		except Exception as _496_:
			_816_(str(_496_), True)
			return _818_('Server internal error:\n' + str(_496_))

def _816_(_496_, _542_):
	_498_ = type(_496_).__name__
	print('Exception type:', _498_)
	if _542_ and _498_ not in ('请登录','数据格式错误','请登录以获取数据','错误的用户名或密码'):
		try:
			import traceback
			print(traceback.format_exc())
		except:
			import sys
			sys.print_exception(_496_)
	return {'error': _498_}

def _514_(_461_, _550_):
	_459_ = _461_._459_
	assert 'object' in _459_, '服务请求参数中缺少 object'
	assert 'method' in _459_, '服务请求参数中缺少 method'
	assert 'data' in _459_, '服务请求参数中缺少 data'
	_277_ = _459_['object']
	_534_ = _459_['method']
	_172_ = json.loads(_459_['data'])
	_544_ = _461_._476_[0]
	return _531_(_277_, _534_, _172_, _461_, _550_)

def _531_(_277_, _534_, _172_, _461_, _550_):
	assert isinstance(_277_, str), '服务请求参数 object 的类型应该是 str 而不是 %s' % type(_172_).__name__
	assert isinstance(_534_, str), '服务请求参数 method 的类型应该是 str 而不是 %s' % type(_172_).__name__
	assert isinstance(_172_, dict), '服务请求参数 data 的类型应该是 dict 而不是 %s' % type(_172_).__name__
	assert _277_ in _550_, '服务器中未注册对象: %s' % _277_
	_277_ = _550_[_277_]
	assert hasattr(_277_, _534_) and callable(getattr(_277_, _534_)), '对象 %s 中没有方法: %s' % (_277_, _534_)
	_172_['request'] = _461_
	_172_['servlets'] = _550_
	return getattr(_277_, _534_)(**_172_)
