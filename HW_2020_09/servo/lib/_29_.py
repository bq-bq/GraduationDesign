
import os

# 获取文件大小
def _846_(_845_):
	_850_ = ['bsize', 'frsize', 'blocks', 'bfree', 'bavail', 'files', 'ffree', ]
	_232_ = dict(zip(_850_, os.statvfs(_845_)))
	return _232_['bsize'] * _232_['bfree']

# 获取文件名
def _244_(*args):
	if type(args[0]) is bytes:
		return b"/".join(args)
	else:
		return "/".join(args)

# 获取文件名 （a/b）-> [a, b]
def _429_(_29_):
	if _29_ == "":
		return ("", "")
	_849_ = _29_.rsplit("/", 1)
	if len(_849_) == 1:
		return ("", _29_)
	_847_ = _849_[0] #.rstrip("/")
	if not _847_:
		_847_ = "/"
	return (_847_, _849_[1])

# 文件名 （a.b） -> [a,.b]
def _554_(_29_):
	if _29_ == "":
		return ("", "")
	_849_ = _29_.rsplit(".", 1)
	if len(_849_) == 1:
		return (_29_, "")
	_849_[1] = "." + _849_[1]
	return (_849_[0], _849_[1])

def _240_(_29_):
	try:
		_848_ = os.stat(_29_)[0]
		return (_848_ & 0o170000) == 0o040000
	except OSError:
		return False

def _22_(_29_):
	try:
		_848_ = os.stat(_29_)[0]
		return (_848_ & 0o170000) == 0o100000
	except OSError:
		return False

def _844_(_29_):
	try:
		os.stat(_29_)
		return True
	except:
		return False

def _512_(_29_):
	return os.stat(_29_)[8]

def _513_(_29_):
	return os.stat(_29_)[6]

_549_ = '/'



