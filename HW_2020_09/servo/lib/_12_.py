



import machine
import time, network, json
from ._19_ import _439_

def _946_():
	_34_ = time.localtime(time.time())
	return '%d/%d/%d %d:%d.%d' % (_34_[0], _34_[1], _34_[2], _34_[3], _34_[4], _34_[5])

class _1_:
	def __init__(_342_):
		_342_._942_ = machine.Pin(22, machine.Pin.OUT)
		_342_.config = None
		_342_._940_()

		_342_._932_ = network.WLAN(network.AP_IF)
		if _342_.config is not None:
			if 'essid' in _342_.config:
				_342_._932_.config(essid=_342_.config['essid'])
			if 'password' in _342_.config:
				_342_._932_.config(password=_342_.config['password'])
		_342_._932_.active(True)
		print('ESP32 本地热点配置:', _342_._932_.ifconfig()) #  _930_ _931_, _941_, _935_, _929_

		_342_._944_ = network.WLAN(network.STA_IF)
		_342_._938_ = None

		_342_._939_ = False
		with open('wifi_index.html') as fp:
			_342_._937_ = fp.read()

		if _342_.config is not None:
			_342_.connect()

	def _940_(_342_):
		try:
			with open('wifi_config.json') as fp:
				_342_.config = json.load(fp)
		except:
			_342_.config = None

	def _943_(_342_):
		with open('wifi_config.json', 'w') as fp:
			json.dump(_342_.config, fp)

	def connect(_342_, _947_=60):
		_342_._942_.on()
		_342_._944_.active(False)
		_342_._944_.active(True)
		_342_._939_ = False
		try:
			_342_._944_.connect(_342_.config['ap_name'], _342_.config['ap_pwd'])
			_342_._938_ = 'ESP32 正在连接 %s ...' % _342_.config['ap_name']
			print(_342_._938_)
		except OSError as _872_:
			_342_._938_ = 'ESP32 异常 ' + str(_872_)
			print(_342_._938_)
			_342_._944_.active(False)
			_342_._942_.on()
			return
		_945_ = time.time()
		while not _342_._944_.isconnected():
			if time.time() - _945_ > _947_:
				break
		if _342_._944_.isconnected():
			_342_._939_ = True
			_342_._942_.off()
			_342_._938_ = '[%s] %s (%s)' % (_342_.config['ap_name'], _342_._944_.ifconfig()[0], _946_())
			print('ESP32 已连接: ', _342_._938_)
		else:
			_342_._938_ = 'ESP32 未能连接到 %s' % _342_.config['ap_name']
			print(_342_._938_)
			_342_._944_.active(False)
			_342_._942_.on()

	def _936_(_342_):
		if _342_.config is None:
			_933_ = _934_ = ''
		else:
			_933_, _934_ = _342_.config['ap_name'], _342_.config['ap_pwd']
		return _342_._937_ % (_933_, _934_, '未连接无线网络' if _342_._938_ is None else _342_._938_)

	def _18_(_342_, _461_, _462_, _464_):
		print('ESP32 连接', _461_._476_)
		_459_ = _461_._459_
		if 'ap_name' in _459_ and 'ap_pwd' in _459_:
			config = {'ap_name':_459_['ap_name'], 'ap_pwd':_459_['ap_pwd']}
			if _342_.config != config:
				_342_.config = config
				_342_._943_()
				_342_.connect()
			else:
				print('ESP32 与已有网络配置相同:', _342_.config['ap_name'])
		_462_._472_(_451_="text/html", _450_=_342_._936_(), _449_='UTF-8')
