
import os, json
from . import db
from .. import lib

def _772_(_773_):
	_768_ = {}
	def _755_(_775_):
		for _266_ in dir(_775_):
			_454_ = getattr(_775_, _266_)
			if _266_.startswith('on_') and callable(_454_):
				_769_ = '@'+_266_[3:]
				_768_[_769_] = _454_
				if _769_.split('_')[0] not in ('@me', '@ui', '@elt', '@pro'):
					print('事件: ' + _769_)
	if _773_:
		print('in this')
		_755_(False)
	else:
		try:
			from .. import services
			for _824_ in dir(services):
				_775_ = getattr(services, _824_)
				if _824_.startswith('__'): continue
				_755_(_775_)
		except:
			pass
	return _768_

class _2_:
	def __init__(_342_, _6_, _11_):
		_342_._550_ = None
		_773_ = 'root_server' not in _6_
		_342_._764_ = _772_('root_server' not in _6_)
		_342_._11_ = _11_
		print(_342_)
		
	def event(_342_, action, event, event_arg, table_names, table_data, as_app, **_417_):
		_445_ = _417_['user_info'][2]
		_774_ = _342_._550_['login']
		_145_ = _774_.has_login(_445_, **_417_)

		while len(table_data) < len(table_names):
			table_data.append(None)
		if as_app == '': as_app = _445_
		assert as_app == _445_, '普通app不能改变身份 %s -> %s' % (_445_, as_app)
		_756_ = _445_ if _145_ is None else _145_
		with db.context(as_app, _756_) as _164_:
			_794_ = {}

			def _793_(_430_, _172_):
				_164_.write(_430_, _172_)
				_794_[_430_] = None
			for _430_, _172_ in zip(table_names, table_data):
				_804_ = (_172_ is None or '__req__' in _172_)
				if _430_[0] != '@':

					assert _164_._227_(_430_), '不存在表格: ' + _430_
					_803_ = _164_._222_(_430_)
					if _803_ != 'public':
						assert _145_ is not None, '请登录以获取数据'
						if _803_ != 'client':
							assert as_app == _756_, '表格<i>%s</i>不能被用户<i>%s</i>访问' % (_430_, _756_)
					elif not _804_:
						assert as_app == _756_, '表格<i>%s</i>不能被用户<i>%s</i>写访问' % (_430_, _756_)
				if _804_: continue
				if _430_[0] == '@':

					assert False, '不支持写入事件%s的返回值' % _430_
				else:
					_761_ = _164_.read(_430_)
					if '__update_time__' not in _761_:
						_761_['__update_time__'] = 0


					_793_(_430_, _172_)

			_754_ = _342_._789_(_445_, _145_, action, event, event_arg, None, _164_)

			def _792_(_430_):
				_761_ = _164_.read(_430_)

				if 'rows' in _761_:
					for _322_ in _761_['rows']:
						for i,c in enumerate(_322_):
							if isinstance(c, float) and c != c:
								_322_[i] = 'NaN'
				if '__update_time__' not in _761_:
					_761_['__update_time__'] = 0
				return _761_
			def _790_(_753_):
				_282_ = _342_._789_(_445_, _145_, _753_, '', '', None, _164_)
				if _282_ is None: return None
				assert isinstance(_282_, dict), '事件<i>%s</i>不是一个表格(返回值:%s)' % (_753_, type(_282_).__name__)
				for _266_ in ('rows', 'field_names', 'field_types'):
					assert _266_ in _282_, '事件<i>%s</i>没有返回值不是一个表格: 缺少 %s' % (_753_, _266_)
				return _282_
			for _430_, _172_ in zip(table_names, table_data):
				if _172_ is None:
					_172_ = { '__update_time__':-1 }
				if _430_[0] == '@':
					if _430_ == action:
						_761_ = _754_
					else:
						_761_ = _790_(_430_)
					if _761_ is not None:
						_761_['__update_time__'] = 0
						_794_[_430_] = _761_
				else:
					_761_ = _792_(_430_)
					if _172_['__update_time__'] < _761_['__update_time__'] or _430_ in _794_:
						_794_[_430_] = _761_
			return _794_

	def _789_(_342_, app, client, action, event, event_arg, data_to_write, _759_):
		if action == '' or action == '@同步':
			return None
		action = action.replace('.', '_')
		print(action)
		if action in _342_._764_:
			_799_ = _342_._764_[action]

			_417_ = {}
			if 'app' not in _417_: _417_['app'] = app
			if 'client' not in _417_: _417_['client'] = client
			if 'action' not in _417_: _417_['action'] = action
			if 'event' not in _417_: _417_['event'] = event
			if 'event_arg' not in _417_: _417_['event_arg'] = event_arg
			if 'data_to_write' not in _417_: _417_['data_to_write'] = data_to_write
			if 'context' not in _417_: _417_['context'] = _759_
			if 'extended_services' not in _417_: _417_['extended_services'] = _342_._764_
			return _799_(**_417_)
		assert False, '服务器中没有定义<i>%s</i>的事件响应程序'%action

