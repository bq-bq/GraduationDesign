
_826_ = _169_ = {}

# 返回本身
def _827_(x):
	return x

for t in (type(None), int, float, bool, str, tuple,
		  type, range, type(Ellipsis)):
	_169_[t] = _827_

#返回 x-> [x][x]
def _828_(x):
	return type(x)(x)
for t in (list, dict, set):
	_169_[t] = _828_

del _169_

def _693_(x, memo=None, _835_=[]):
	if memo is None:
		memo = {}
    #获取 x 的id
	_169_ = id(x)
	_843_ = memo.get(_169_, _835_)
	if _843_ is not _835_:
		return _843_

	_838_ = type(x)

	_839_ = _831_.get(_838_)
	if _839_:
		_843_ = _839_(x, memo)
	else:
		assert issubclass(_838_, type)
		_843_ = _829_(x, memo)

	if _843_ is not x:
		memo[_169_] = _843_
		_834_(x, memo) # _825_ _842_ x _841_ _837_ _840_ as long as _169_
	return _843_

_831_ = _169_ = {}

def _829_(x, memo):
	return x
_169_[type(None)] = _829_
_169_[type(Ellipsis)] = _829_
_169_[int] = _829_
_169_[float] = _829_
_169_[bool] = _829_
try:
	_169_[complex] = _829_
except NameError:
	pass
_169_[bytes] = _829_
_169_[str] = _829_
_169_[type] = _829_
_169_[range] = _829_

def _832_(x, memo):
	_843_ = []
	memo[id(x)] = _843_
	for _836_ in x:
		_843_.append(_693_(_836_, memo))
	return _843_
_169_[list] = _832_

def _833_(x, memo):
	_843_ = []
	for _836_ in x:
		_843_.append(_693_(_836_, memo))
	try:
		return memo[id(x)]
	except KeyError:
		pass
	for i in range(len(x)):
		if x[i] is not _843_[i]:
			_843_ = tuple(_843_)
			break
	else:
		_843_ = x
	return _843_
_169_[tuple] = _833_

def _830_(x, memo):
	_843_ = type(x)()
	memo[id(x)] = _843_
	for key, value in x.items():
		_843_[_693_(key, memo)] = _693_(value, memo)
	return _843_
_169_[dict] = _830_

def _834_(x, memo):
	try:
		memo[id(memo)].append(x)
	except KeyError:
		memo[id(memo)]=[x]
