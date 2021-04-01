
import os, socket, gc, json, time, sys
from ._29_ import _844_

class _856_:
	def __init__(_342_, _463_, _534_, _814_, _454_, _464_):
		_342_._463_ = _463_
		_342_._534_ = _534_
		_342_._814_ = _814_
		_342_._454_ = _454_
		_342_._464_ = _464_

_885_ = {
	".txt"  : "text/plain",
	".htm"  : "text/html",
	".html" : "text/html",
	".css"  : "text/css",
	".csv"  : "text/csv",
	".py"	: "application/python",
	".js"	: "application/javascript",
	".xml"  : "application/xml",
	".xhtml": "application/xhtml+xml",
	".json" : "application/json",
	".zip"  : "application/zip",
	".pdf"  : "application/pdf",
	".ts"	: "application/typescript",
	".woff" : "font/woff",
	".woff2": "font/woff2",
	".ttf"  : "font/ttf",
	".otf"  : "font/otf",
	".jpg"  : "image/jpeg",
	".jpeg" : "image/jpeg",
	".png"  : "image/png",
	".gif"  : "image/gif",
	".svg"  : "image/svg+xml",
	".ico"  : "image/x-icon"
}
# 获取 以_885_结尾的文件名
def _874_(_415_):
	print(_415_)
	_415_ = _415_.lower()
	for _499_ in _885_:
		if _415_.endswith(_499_):
			return _885_[_499_]
	return None

# 使用utf-8编码以及解码 返回源字符串的utf-8 编码
def _906_(_668_):
	_304_ = str(_668_).split('%')
	try:
		b = _304_[0].encode()
		for i in range(1, len(_304_)):
			try:
				b += bytes([int(_304_[i][:2], 16)]) + _304_[i][2:].encode()
			except:
				b += b'%' + _304_[i].encode()
		return b.decode('UTF-8')
	except:
		return str(_668_)

# 返回将‘+’换为 ‘ ’的utf-8 编码字符串
def _907_(_668_):
	return _906_(_668_.replace('+', ' '))



class _439_:# _342_ is self
	_857_ = 2
	_851_ = 16 # _928_

	def __init__(_342_, _20_, _460_, _469_, _28_):
		_342_._596_ = (_20_, _460_)
		if _469_.endswith('/'):
			_469_ = _469_[:-1]
		_342_._469_ = _469_
		_342_._902_ = False
		_342_._28_ = _28_
		_342_._904_ = 0
		_342_._898_ = []

	def _442_(_342_, _909_, _454_, _534_='GET', _814_=''):
		if _909_.startswith('/'):
			_909_ = _909_[1:]
		if _909_.endswith('/'):
			_909_ = _909_[:-1]
		_899_ = _909_.split('/')
		_464_ = []
		for _668_ in _899_:
			if _668_.startswith('{') and _668_.endswith('}'):
				_464_.append(_668_[1:-1])
		_342_._898_.append(_856_(_899_, _534_, _814_, _454_, _464_))

	def _875_(_342_, _909_, _534_, _814_):
		if _909_.startswith('/'):
			_909_ = _909_[1:]
		if _909_.endswith('/'):
			_909_ = _909_[:-1]
		_899_ = _909_.split('/')
		_534_ = _534_.upper()
		def _884_(_899_, _909_):
			if len(_899_) != len(_909_):
				return None
			_6_ = {}
			for _908_, _905_ in zip(_899_, _909_):
				if _908_.startswith('{') and _908_.endswith('}'):
					_6_[_908_[1:-1]] = _905_
				elif _908_ != _905_:
					return None
			return _6_
		for _896_ in _342_._898_:
			if _896_._534_ == _534_ and _814_.startswith(_896_._814_):
				_6_ = _884_(_896_._463_, _909_.split('/'))
				if _6_ is not None:
					return _896_._454_, _6_
		return None, None

	def _350_(_342_):
		assert not _342_._902_
		_342_._32_ = socket.socket()
		_342_._32_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		_342_._32_.bind(_342_._596_)
		_342_._32_.listen(_439_._851_)
		_342_._902_ = True
		while True:
			try:
				_860_, _814_ = _342_._32_.accept()
			except KeyboardInterrupt as _496_:
				break
			except Exception as _496_:
				print(_496_.args)
				sys.print_exception(_496_)
				continue


			if _342_._28_ == 0:
				_342_._904_ += 1
				_342_._861_(_860_, _814_)
			else:
				import _thread
				try:
					_thread.start_new_thread(_342_._861_, (_860_, _814_))
					_342_._904_ += 1
				except OSError as _872_:
					print(str(_872_))
				while _342_._904_ >= _342_._28_:
					time.sleep(0.1)
		_342_._902_ = False

	def _861_(_342_, _860_, _814_):
		_854_(_342_, _860_, _814_)
		_342_._904_ -= 1

	def _903_(_342_):
		if _342_._902_:
			_342_._32_.close()

	def _881_(_342_):
		return _342_._902_

	def _882_(_342_, _909_):
		if _909_[0] == '/':
			_909_ = _909_[1:]
		if not _909_.startswith('web/'):
			return None
		_909_ = _909_[4:]
		_29_ = _342_._469_ + '/' + _909_.replace('../', '/')
		if _844_(_29_):
			return _29_
		return None



def _889_(_891_, _866_='&', _867_='='):
	_459_ = {}
	_869_ = _891_.split(_866_)
	for _868_ in _869_:
		_540_ = _868_.split(_867_, 1)
		if len(_540_) > 0:
			_910_ = _540_[1] if len(_540_) > 1 else ''
			_459_[_540_[0]] = _910_
	return _459_

def _878_(_872_):
	if hasattr(sys, 'print_exception'):
		sys.print_exception(_872_)
	else:
		import traceback
		traceback.print_exc()
		del traceback

class _854_:

	def __init__(_342_, _19_, _900_, _476_):
		_900_.settimeout(2)
		_342_._19_ = _19_
		_342_._900_ = _900_
		_342_._476_ = _476_
		_342_._534_ = None
		_342_._29_ = None
		_342_._880_ = None
		_342_._459_ = {}
		_342_._877_ = {}
		_342_._451_ = None
		_342_._863_ = 0

		if hasattr(socket, 'readline'): # _853_
			_342_._901_ = _342_._900_
		else: # _852_
			_342_._901_ = _342_._900_.makefile('rwb')

		try:
			_462_ = _855_(_342_)
			if _342_._887_():
				if _342_._888_():
					_342_._893_()
					_897_, _464_ = _342_._19_._875_(_342_._29_, _342_._534_, _342_._476_[0])
					if _897_:
						try:
							_897_(_342_, _462_, _464_)
						except Exception as _496_:
							print('Http handler exception in route %s %s\r\n' % (_342_._534_, _342_._29_))
							_878_(_496_)
							raise _496_
					else:
						_342_._470_(_462_)
				else:
					_462_._919_()
		except Exception as _496_:
			_878_(_496_)
			_462_._923_()
		finally:
			try:
				if _342_._901_ is not _342_._900_:
					_342_._901_.close()
				_342_._900_.close()
			except:
				print('Exception while closing socket_file')
				pass

	def _887_(_342_):
		try:
			_869_ = _342_._901_.readline().decode().strip().split()
			if len(_869_) == 3:
				_342_._534_  = _869_[0].upper()
				_342_._29_	= _869_[1]
				_342_._880_ = _869_[2].upper()
				_869_ = _342_._29_.split('?', 1)
				if len(_869_) > 0:
					_342_._29_ = _907_(_869_[0])
				if len(_869_) > 1:
					_459_ = _889_(_869_[1])
					_342_._459_ = {_907_(k):_907_(v) for k,v in _459_.items()}
				return True
		except:
			pass
		return False

	def _888_(_342_):
		while True:
			_869_ = _342_._901_.readline().decode().strip().split(':', 1)
			if len(_869_) == 2:
				_342_._877_[_869_[0].strip().lower()] = _869_[1].strip()
			elif len(_869_) == 1 and len(_869_[0]) == 0:
				if _342_._534_ == 'POST' or _342_._534_ == 'PUT':
					_342_._451_   = _342_._877_.get("content-type", None)
					_342_._863_ = int(_342_._877_.get("content-length", 0))
				return True
			else:
				return False

	def _892_(_342_, _552_=None):
		if _552_ is None:
			_552_ = _342_._863_
		if _552_ > 0:
			try:
				return _342_._901_.read(_552_)
			except:
				pass
		return b''

	def _893_(_342_):
		if 'content-type' not in _342_._877_:
			return
		_172_ = _342_._892_()
		if _342_._877_['content-type'] == 'application/x-www-form-urlencoded':
			_172_ = _172_.decode()
			_172_ = _889_(_172_)
			_172_ = {_907_(k):_907_(v) for k,v in _172_.items()}
			_342_._459_.update(_172_)
		elif _342_._877_['content-type'].startswith('multipart/form-data;'):
			_858_ = _342_._877_['content-type'].split(';')[1].split('=')[1]
			_858_ = '--' + _858_
			_172_ = _172_.split(_858_.encode())
			_172_ = _172_[1:-1]
			for _487_ in _172_:
				_487_ = _487_[2:-2].split(b'\r\n\r\n')
				assert _487_[0].startswith(b'Content-Disposition: form-data; ')
				_890_ = _487_[0].decode().split('; ', 1)[1]
				_529_ = _890_.split('\r\n')
				if len(_529_) == 1:
					_865_ = _889_(_907_(_529_[0]), '; ')
					assert len(_865_) == 1 and 'name' in _865_, _890_
					_266_ = json.loads(_865_['name'])
					_342_._459_[_266_] = _487_[1].decode()
				else:
					assert len(_529_) == 2, _890_
					_865_ = _889_(_907_(_529_[0]), '; ')
					assert len(_865_) == 2 and 'name' in _865_ and 'filename' in _865_, _890_
					_266_ = json.loads(_865_['name'])
					_415_ = json.loads(_865_['filename'])
					_342_._459_[_266_] = {'filename':_415_, 'file':_487_[1]}
		else:
			assert False, 'Content-type unsupported: %s' % _342_._877_['content-type']

	def _470_(_342_, _462_, _29_=None):
		if _29_ is None:
			_29_ = _342_._29_
		_873_ = _342_._19_._882_(_29_)
		if _873_:
			_451_ = _874_(_873_)
			if _451_:
				if _439_._857_ > 0:
					if _439_._857_ > 1 and 'if-modified-since' in _342_._877_ and '__temp__' not in _29_:
						_462_._925_()
					else:
						_877_ = { 'Last-Modified': 'Fri, 1 Jan 2021 00:00:00 GMT', \
									'Cache-Control': 'max-age=315360000' }
						_462_._921_(_873_, _451_, _877_)
				else:
					_462_._921_(_873_, _451_)
			else:
				_462_._922_()
		else:
			_462_._473_()



_879_ = {
	200: ('OK', 'Request fulfilled, document follows'),
	302: ('Found', 'Object moved temporarily -- see URI list'),
	304: ('Not Modified', 'Document has not changed since given time'),
	400: ('Bad Request','Bad request syntax or unsupported method'),
	403: ('Forbidden','Request forbidden -- authorization will not help'),
	404: ('Not Found', 'Nothing matches the given URI'),
	405: ('Method Not Allowed', 'Specified method is invalid for this resource.'),
	500: ('Internal Server Error', 'Server got itself in trouble'),
}

class _855_:

	def __init__(_342_, _461_):
		_342_._461_ = _461_

	def _911_(_342_, _172_, _870_='ISO-8859-1'):
		if _172_:
			if type(_172_) == str:
				_172_ = _172_.encode(_870_)
			_172_ = memoryview(_172_)
			while _172_:
				_886_ = _342_._461_._901_.write(_172_)
				if _886_ is None:
					return False
				_172_ = _172_[_886_:]
			return True
		return False

	def _915_(_342_, _862_):
		_894_ = _879_.get(_862_, ('Unknown reason', ))[0]
		return _342_._911_("HTTP/1.1 %s %s\r\n" % (_862_, _894_))

	def _916_(_342_, _266_, _910_):
		return _342_._911_("%s: %s\r\n" % (_266_, _910_))

	def _913_(_342_, _451_, _449_=None):
		if _451_:
			_864_ = _451_ + (("; charset=%s" % _449_) if _449_ else "")
		else:
			_864_ = "application/octet-stream"
		_342_._916_("Content-Type", _864_)

	def _926_(_342_):
		_342_._916_("Server", "ESP-6288")

	def _914_(_342_):
		return _342_._911_("\r\n")

	def _912_(_342_, _862_, _877_, _451_, _449_, _863_):
		_342_._915_(_862_)
		if isinstance(_877_, dict):
			for _876_ in _877_:
				_342_._916_(_876_, _877_[_876_])
		if _863_ > 0:
			_342_._913_(_451_, _449_)
			_342_._916_("Content-Length", _863_)
		_342_._926_()
		_342_._916_("Connection", "close")
		_342_._914_()

	def _917_(_342_, _862_, _877_, _451_, _449_, _450_):
		try:
			if _450_:
				if type(_450_) == str:
					_450_ = _450_.encode(_449_)
				_863_ = len(_450_)
			else:
				_863_ = 0
			_342_._912_(_862_, _877_, _451_, _449_, _863_)
			if _450_:
				return _342_._911_(_450_)
			return True
		except:
			try:
				import traceback
				print(traceback.format_exc())
			except:
				pass
			return False

	def _921_(_342_, _873_, _451_=None, _877_=None):
		try:
			_552_ = os.stat(_873_)[6]
			if _552_ > 0:
				with open(_873_, 'rb') as _412_:
					_342_._912_(200, _877_, _451_, None, _552_)
					try:
						_859_ = bytearray(256)
						while _552_ > 0:
							_927_ = _412_.readinto(_859_)
							if _927_ < len(_859_):
								_859_ = memoryview(_859_)[:_927_]
							if not _342_._911_(_859_):
								return False
							_552_ -= _927_
						return True
					except:
						_342_._923_()
						return False
		except:
			pass
		_342_._473_()
		return False

	def _472_(_342_, _877_=None, _451_=None, _449_=None, _450_=None):
		return _342_._917_(200, _877_, _451_, _449_, _450_)

	def _471_(_342_, _458_='{}', _877_=None):
		return _342_._917_(200, _877_, "application/json", "UTF-8", _458_)

	def _474_(_342_, _883_):
		_877_ = { "Location": _883_ }
		return _342_._917_(302, _877_, None, None, None)

	def _920_(_342_, _862_, _871_=None):
		_895_ = '[%(code)d %(reason)s] %(message)s'
		_894_, _702_ = _879_.get(_862_, ('Unknown reason', ''))
		if _871_ is not None:
			_702_ = _871_
		_871_ = _895_ % {'code': _862_, 'reason':_894_, 'message':_702_}
		return _342_._917_(_862_, None, "text/html", "UTF-8", _871_)

	def _918_(_342_, _862_, _458_='{}'):
		return _342_._917_(_862_, None, "application/json", "UTF-8", _458_)

	def _925_(_342_):
		return _342_._920_(304)

	def _919_(_342_):
		return _342_._920_(400)

	def _922_(_342_):
		return _342_._920_(403)

	def _473_(_342_):
		return _342_._920_(404)

	def _924_(_342_):
		return _342_._920_(405)

	def _923_(_342_, _702_=None):
		return _342_._920_(500, _702_)

