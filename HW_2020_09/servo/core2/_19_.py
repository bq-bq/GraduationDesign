
import json

def _456_(_461_, _462_, _464_):
	global _457_
	_447_(_457_, _461_, _462_);

def _444_(_461_, _462_, _464_):
	global _32_
	_458_ = _32_._443_(_461_)
	_458_ = json.dumps(_458_)
	return _462_._471_(_458_)

def _445_(_461_, _462_, _464_):
	_448_ = _464_['appname']
	if _448_.endswith('.py'):
		return _462_._474_('web/' + _448_)
	return _447_(_448_, _461_, _462_)

def _412_(_461_, _462_, _464_):
	global _32_
	_448_ = _464_['appname']
	_415_ = _464_['filename']
	if _448_ == 'web':
		return _461_._470_(_462_, '%s/%s' % (_448_, _415_))
	else:
		return _461_._470_(_462_, 'web/user_data/%s/%s' % (_448_, _415_))

def _447_(_448_, _461_, _462_):
	global _32_
	if not _32_._446_(_448_, _462_._461_._459_):
		return _462_._473_()
	return _461_._470_(_462_, _32_._813_)

_32_=None
_457_ = 'not_defined'

def _33_(_441_, _460_, _440_, _28_, _13_=None):
	from ..lib._19_ import _439_
	global _457_, _32_
	_32_ = _441_
	_457_ = _440_
    #def __init__(_20_, _460_, _469_, _28_):
	_19_ = _439_(_20_='0.0.0.0', _460_=_460_, _469_='web', _28_=_28_)
	if _13_ is not None:
		_19_._442_('/', _13_, _814_='192.168.4.')
	_19_._442_('/', _456_)
	_19_._442_('/ajax', _444_, 'GET')
	_19_._442_('/ajax', _444_, 'POST')
	_19_._442_('/{appname}', _445_)
	_19_._442_('/{appname}/{filename}', _412_)
	_19_._442_('/{appname}/{filename}', _412_, 'POST')
	_19_._350_()
