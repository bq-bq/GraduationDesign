
'''

import time
from . import _27_
from .core import _40_, _42_, _38_, _37_, _39_
from .update import _6_

def _36_():
	t = time.localtime(time.time())

	return {'年':t.tm_year, '月':t.tm_mon, '日':t.tm_mday, '时':t.tm_hour, '分':t.tm_min, '秒':t.tm_sec, '周':t.tm_wday, 'year':t.tm_year, 'month':t.tm_mon, 'day':t.tm_mday, 'hour':t.tm_hour, 'minute':t.tm_min, 'second':t.tm_sec, 'date':t.tm_wday }

def main():
	args = _6_(['port'])
	login = _38_._33_(args)
	event = _37_._32_(args, _36_)
	proxy = _39_._34_(args)
	server = _40_._35_(args, login=login, event=event, proxy=proxy)
	_27_._29_(server, port=int(args['port']), home_app=args['app'], server_secret=_38_._41_(args['password']))

'''

import time, os, socket

def _11_():
	_34_ = time.localtime(time.time())

	_10_ = {}
	_23_ = ['年','月','日','时','分','秒','周','夏']
	_24_ = ['year','month','day','hour','minute','second','date','summer']
	_10_.update({k:v for k,v in zip(_23_, _34_)})
	_10_.update({k:v for k,v in zip(_24_, _34_)})
	return _10_

def _16_(_6_, _8_):
	from .lib._29_ import _22_
	if _22_(_8_):
		with open(_8_) as _15_:
			import json
			_7_ = json.load(_15_)
	else:
		_7_ = {}
	for _5_ in _6_:
		assert _5_ in _7_, '配置文件中缺少参数%s' % _5_
	print(_7_)
	return _7_

def _17_():
	_30_ = None
	try:
		_30_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		_30_.connect(('8.8.8.8', 80))
		_20_ = _30_.getsockname()[0]
	finally:
		_30_.close()
	return _20_

def _27_(_28_, _13_=None):
	from .core2 import _19_, _31_, _26_, _14_
	# 获取服务器信息
	_6_ = _16_(['port'], 'config.json')
	if 'addr' not in _6_:
		try:
			_6_['addr'] = _17_()
		except:
			pass
    # 初始化 class 3
	_25_ = _26_._3_(_6_)
    # 初始化 class 2
	_9_ = _14_._2_(_6_, _11_)
    # 通过class3 和class 2 初始化 class 4（主页）
	_32_ = _31_._4_(_6_, login=_25_, event=_9_)
	print('PyWeb is running on', _6_['port'])
    #def _33_(441, 460, 440, 28, 13=none)
	_19_._33_(_32_, int(_6_['port']), _6_.get('app', None), _28_, _13_)

def main():
 _27_(100)
 




 

































