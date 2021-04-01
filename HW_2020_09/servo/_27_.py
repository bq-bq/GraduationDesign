
import os
from pyramid.view import (view_config, view_defaults)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response, FileResponse
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator
from waitress import serve

def start(port, server_secret):
	session_factory = SignedCookieSessionFactory(server_secret)
	with Configurator(session_factory=session_factory) as config:
		config.add_route('home', '/')
		config.add_route('upload', '/upload')
		config.add_route('ajax', '/ajax')
		config.add_route('app', '/{appname}')
		config.add_route('app2', '/{appname}/')
		config.add_route('file', '/{appname}/{filename}')
		config.add_static_view(name='web', path='../web')
		config.scan('.')
		app = config.make_wsgi_app()
		serve(app, host='0.0.0.0', port=port, threads=100)


@view_defaults(renderer='json')
class _16_:
	def __init__(_28_, request):
		_28_.request = request

	@view_config(route_name='upload')
	def _31_(_28_):
		global _18_
		return _18_._31_(_28_.request)

	@view_config(route_name='ajax')
	def _19_(_28_):
		global _18_
		return _18_._19_(_28_.request)

	@view_config(route_name='app')
	def app(_28_):
		_23_ = _28_.request.matchdict['appname']
		if _23_.endswith('.py'):
			raise HTTPFound(location=os.path.join('web', _23_))
		return _28_._21_(_23_)

	@view_config(route_name='app2')
	def _20_(_28_):
		_23_ = _28_.request.matchdict['appname']
		raise HTTPFound(location=_23_)

	@view_config(route_name='file')
	def file(_28_):
		_23_ = _28_.request.matchdict['appname']
		filename = _28_.request.matchdict['filename']
		_24_ = os.path.join(_23_, filename)
		if _23_ == 'web' and os.path.isfile(_24_):

			return FileResponse(_24_, _28_.request)
		elif _23_ == 'ui' and filename == 'update.zip':
			_30_ = _18_._25_(_28_.request)
			return Response(body=_30_, content_type='application/zip')
		else:
			_24_ = os.path.join('web', 'user_data', _24_)
			if os.path.isfile(_24_):
				return FileResponse(_24_, _28_.request)
			raise HTTPNotFound(_23_+'/'+filename)


	@view_config(route_name='home')
	def _26_(_28_):
		global _17_
		return _28_._21_(_17_);

	def _21_(_28_, _22_):
		global _18_
		response = _18_._21_(_22_)
		if response is None:
			raise HTTPNotFound(_22_)
		_28_.request.response.text = response
		return _28_.request.response

_18_=None
_17_ = 'not_found'

def _29_(server, port, home_app, server_secret):
	global _18_, _17_
	_18_ = server
	_17_ = home_app
	start(port=port, server_secret=server_secret)
