
import os, json, random
from .db import context
from .. import lib

def _591_(_246_, _577_='abcdefghijklmnopqrstuvwxyz0123456789'):
	return ''.join([_577_[random.randint(0,len(_577_)-1)] for i in range(_246_)])

def _578_(_445_, _564_, _581_):
	if _564_ is None: return False
	with context(app=_445_, client=_445_) as _136_:

		assert _136_._820_('用户组'), '应用<i>%s</i>中未定义表格<i>用户组</i>'%_445_
		_822_ = _136_.read('用户组')
		assert _822_['field_names'] == ['用户组', '用户名'], '应用<i>%s</i>的表格<i>用户组</i>中缺少<i>用户名</i>或<i>组名</i>'%_445_
		for _823_, _819_ in _822_['rows']:
			if _823_ == _564_ and _819_ == _581_: return True
		return False

def _595_(_596_, _587_, _534_, **kwargs__):
	try:
		import requests
	except:
		import _821_ as requests
	_596_ = _596_ or 'localhost'
	_172_ = {'object':_587_, 'method':_534_, 'data':json.dumps(kwargs__)}
	_462_ = requests.post('http://%s/ajax'%_596_, data=_172_, verify=False)
	context = _462_.content.decode('utf-8')
	return ''
	return json.loads(context)

def _583_(_592_, _565_):
	_565_=[_565_['user'], _565_['session_code'], _565_['app'], _565_['app_secret']]
	_462_ = _595_(_592_, 'login', 'has_login', user_info=_565_)
	return _462_ is not None


class _3_:
	def __init__(_342_, _6_):
		_342_._6_ = _6_
		_342_._550_ = None
		_342_._597_ = {}
		_342_._576_ = {}

	def has_login(_342_, app=None, **_417_):

		_565_ = _417_.get('user_info', None)
		assert _565_ is not None, 'Missing user info'
		_564_, _597_, _445_, _575_ = _565_
		if app is not None:
			if app != _445_: return None
		if _564_ == '': return None
		assert 'root_server' in _342_._6_, '缺少运行必须的参数 root_server'
		if _564_ in _342_._576_ and _445_ in _342_._576_[_564_]:
			if _342_._576_[_564_][_445_] == _575_: return _564_
		_547_ = _342_._6_['root_server']
		_565_ = {'user':_564_, 'session_code':_597_, 'app':_445_, 'app_secret':_575_}
		if _583_(_547_, _565_):
			if _564_ not in _342_._576_: _342_._576_[_564_] = {}
			_342_._576_[_564_][_445_] = _575_
			return _564_
		return None

	def logout(_342_, **kwargs__):
		_602_ = _342_.has_login(**kwargs__)
		if _602_ is not None:
			if _602_ in _342_._597_:
				del _342_._597_[_602_]
			if _602_ in _342_._576_:
				del _342_._576_[_602_]
		return {}

	def login_with_pwd(_342_, **_417_):
		print(_342_)
		print(_417_)
		_565_ = _417_.get('user_info', None)
		_564_ = _417_.get('user',None)
		_597_ = _417_.get('pwd',None)
		_445_ = _417_.get('app',None)
		_575_ = _417_.get('app_secret',None)
		print(_445_)
		if _564_ == '': return None
		assert 'root_server' in _342_._6_, '缺少运行必须的参数 root_server'
		if _564_ in _342_._576_ and _445_ in _342_._576_[_564_]:
			if _342_._576_[_564_][_445_] == _575_: return _564_
		_547_ = _342_._6_['root_server']
		_565_ = {'user':_564_, 'session_code':_597_, 'app':_445_, 'app_secret':_575_}
		return _565_
    
	def get_app_info(_342_, app, **kwargs__):
		_602_ = _342_.has_login(app, **kwargs__)
		_585_ = (_602_ is not None)
		_586_ = (_602_ is not None and _602_ == app)
		if app != 'ui' and not lib._29_._240_(lib._29_._244_('user_db', 'ui', 'clients', app)):
			return {'brand':'404 找不到网页', 'activities':[]}
		with context(app='ui', client=app) as _136_:


			_538_ = _136_.read('page')['rows']
		_573_ = []
		for i, _537_ in enumerate(_538_):
			_600_ = _537_[1].split(',')
			if _600_[0] in ('login','登录后') and not _585_: continue
			if _600_[0] in ('logout','登录前') and _585_: continue
			if _600_[0] in ('owner', '网站作者') and not _586_: continue
			if _600_[0] == '用户组':
				if len(_600_) < 2: continue
				_581_ = _600_[1].strip()
				if not _578_(app, _602_, _581_): continue
			_573_.append({'id':'activity_%d' % (i+1), 'name':_537_[0], 'ui_json':_537_[2]})
		return {'user':(_602_ if _602_ is not None else ''), 'activities':_573_}

