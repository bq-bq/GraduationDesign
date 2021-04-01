import time, json, os
from .. import lib

# 获取数字
def _371_(_384_):
	if _384_ is None or _384_ == '': return float('NaN')
	try:
		return int(_384_)
	except:
		pass
	try:
		return float(_384_)
	except:
		return None

# 日期->字符串
def time_to_text(_349_):

	_384_ = '%04d-%02d-%02d %02d:%02d:%02d' % time.localtime(int(_349_))[:6]
	if _384_.endswith(' 00:00:00'): return _384_.split()[0]
	if _384_.startswith('1900-01-01 '): return _384_.split()[1]
	return _384_

#  日期->对应秒数
def _372_(_384_):
	_175_ = ('', '%d %b %y', '%Y-%m-%d', '%d-%b-%Y', '%m/%d/%Y', '%Y.%m.%d', '%Y.%m', '%Y年%m月%d日', '%m月%d日', '%Y年%m月%d号', '%Y年%m月', '%Y', '%Y年', '%m月')
	_374_ = ('', '%I:%M%p', '%H:%M:%S', '%H:%M', '%M:%S', '%H:%M:%S.%f', '%H:%M:%S.%f', '上午%H:%M', '下午%H:%M')
	for _174_ in _175_:
		for _373_ in _374_:
			_176_ = (_174_ + ' ' + _373_).strip()
			try:
				_383_ = time.strptime(_384_, _176_)
				_383_ = time.mktime(_383_)
				if _373_.startswith('下午'):
					_383_ += 43200
				return _383_
			except ValueError:
				pass
			except OverflowError:
				pass
	assert False, '数据格式错误: 不能转换为类型 time: %s' % _384_

# 获取（TRUE/FALSE/NONE）
def _370_(_384_):
	_282_ = _384_.lower()
	assert _282_ in ('true', 'false', ''), '数据格式错误: 不能转换为类型 boolean: %s' % _384_
	return (_282_ == 'true')


_88_ = {'text':(str,), 'number':(int,float), 'time':(int,float), 'boolean':(bool,)}
def _139_(_169_, _158_, _280_=None, info=None):
	if (_169_ is not None) and (type(_169_) in _88_[_158_]):
		return _169_
	if _158_ == 'boolean':
		if isinstance(_169_, str):
			return _370_(_169_)
		if isinstance(_169_, int):
			assert _169_ in (0,1), '数据格式错误: 不能转换为类型 bool: %d'%_169_
			return _169_ == 1
		assert isinstance(_169_, bool)
		return _169_
	elif _158_ == 'number':
		_274_ = _371_(_169_)
		assert _274_ is not None, '数据格式错误: %s 不能转换为类型 number: \'%s\'' % (_169_, '' if info is None else ':\n'+info)
		return _274_
	elif _158_ == 'text':
		if _169_ is None: return ''
		if _280_ == 'time':
			return time_to_text(_169_)
		else:
			return str(_169_)
	elif _158_ == 'time':
		if _169_ is None: return -2209017943.0
		if isinstance(_169_, str):
			return _372_(_169_)
		assert isinstance(_169_, (int, float))
		return _169_
	else:
		assert False, 'Unknown type: ' + _158_

def _138_(_169_, _158_):
	if _158_ == 'time':
		return time_to_text(_169_)
	return str(_169_)

import _thread
_808_ = _thread.allocate_lock()


class context:
    # db 所处位置及其事务
	__CONSISTENT_COMMIT__ = lib._29_._244_('user_db', '__transaction_commit__')

	def __init__(_342_, app, client):
		_342_.app = app
		_342_.client = client
		_342_._338_ = None

	def _109_(_342_, _360_, _145_=None):
		_363_ = ''
		if _360_ != '__schema__':
			_363_ = _342_._222_(_360_)
		assert _363_ != 'virtual'
		if _145_ is None:
			_145_ = _342_.client
		_124_ = lib._29_._244_('user_db', _342_.app)
		if not lib._29_._240_(_124_):
			os.mkdir(_124_)
		if _363_ in ('', 'public', 'big') or _342_.app == _145_:
			_361_ = lib._29_._244_(_124_, _360_+'.json')
		elif _363_ == 'client':
			assert _145_ is not None, 'Client table \'%s\' requires user login.' % _360_
			_146_ = lib._29_._244_(_124_, 'clients')
			if not lib._29_._240_(_146_):
				os.mkdir(_146_)
			_146_ = lib._29_._244_(_146_, _145_)
			if not lib._29_._240_(_146_):
				os.mkdir(_146_)
			_361_ = lib._29_._244_(_146_, '%s.json' % _360_)
		else:
			raise AssertionError('Unknown table type: \'%s\'' % _363_)
		return _361_

	def _227_(_342_, _360_):
		if _342_._338_ is not None:
			return _360_ in _342_._338_
		_361_ = _342_._109_(_360_)
		return lib._29_._22_(_361_)

	def _222_(_342_, _360_):
		if _342_._338_ is None:
			assert (_342_.app == 'ui' and _360_ == 'page') or \
				(_342_.app == 'me' and _360_ == 'settings'), '应用%s缺少数据库纲要' % _342_.app
			return 'client'
		assert _360_ in _342_._338_, '应用%s不存在表格%s' % (_342_.app, _360_)
		return _342_._338_[_360_]['table_type']

	def _218_(_342_, _360_, _172_):
		if _342_._338_ is not None:
			_34_ = _342_._338_[_360_]
			return _34_['field_names'], _34_['field_types']
		return _172_['field_names'], _172_['field_types']

	def read(_342_, _360_, _361_=None):
		if _361_ is None:
			_361_ = _342_._109_(_360_)
		assert lib._29_._22_(_361_), '不存在表格: ' + _360_
		with open(_361_, encoding="UTF-8") as _15_:
			_172_ = json.load(_15_)
		if 'rows' in _172_:
			_150_, _151_ = _342_._218_(_360_, _172_)
			for _304_,_322_ in enumerate(_172_['rows']):
				for i, (_169_, t) in enumerate(zip(_322_, _151_)):
					_322_[i] = _139_(_169_, t, info='table:%s, col:%s, row:%d, col_type:%s'%(_360_,_150_[i],_304_,t))
		return _172_

	def write(_342_, _360_, _172_, _361_=None):
		if _361_ is None:
			_361_ = _342_._109_(_360_)
		_810_ = int(_172_['__update_time__'] if '__update_time__' in _172_ else 0)
		_172_['__update_time__'] = int(time.time())
		if _810_ >= _172_['__update_time__']:
			_172_['__update_time__'] = _810_ + 1


		_812_(_172_, _361_)
		_811_()

	def __enter__(_342_):
		global _808_
		_808_.acquire()
		_361_ = lib._29_._244_('user_db', _342_.app, '__schema__.json')
		if lib._29_._22_(_361_):
			with open(_361_,encoding='utf-8') as _15_:
				_342_._338_ = json.load(_15_)
		return _342_

	def __exit__(_342_, _195_, _196_, trace):
		_808_.release()
		return _196_ is None

# 选择所写入的文件
def _812_(_458_, _29_):
	if not lib._29_._240_(context.__CONSISTENT_COMMIT__):
		os.mkdir(context.__CONSISTENT_COMMIT__)
	_809_ = lib._29_._244_(context.__CONSISTENT_COMMIT__, 'plan.txt')
	_807_ = lib._29_._244_(context.__CONSISTENT_COMMIT__, 'tmp.json')
	with open(_807_, 'w') as _15_:
		json.dump(_458_, _15_)
	with open(_809_, 'w') as _15_:
		_15_.write(_29_ + '\n##')
# 写入文件 通过 plan 选择 tmp -> 目标
def _811_():
    # _事务文件夹
	if not lib._29_._240_(context.__CONSISTENT_COMMIT__):
		os.makedirs(context.__CONSISTENT_COMMIT__)
	_809_ = lib._29_._244_(context.__CONSISTENT_COMMIT__, 'plan.txt')
	_807_ = lib._29_._244_(context.__CONSISTENT_COMMIT__, 'tmp.json')
	if not lib._29_._22_(_809_): return
	if not lib._29_._22_(_807_): return
	with open(_809_) as fp:
		lines = fp.readlines();
	if len(lines) != 2 or lines[1] != '##': return
	if os.path.isfile(lines[0].strip()):
		os.remove(lines[0].strip())
	os.rename(_807_, lines[0].strip())
	os.remove(_809_)

_811_()
