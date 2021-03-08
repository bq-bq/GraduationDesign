

import bottle
import os
import sys


import routes
# bottle 默认启动模式
def wsgi_app():
    return bottle.default_app()

'''启动Bottle服务器 
	ROJECT_ROOT 服务器地址
	STATIC_ROOT 静态文件根地址
	HOST 主机地址
	PORT 端口地址（此处选用8888端口）'''
def main():
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    print(PROJECT_ROOT)
    print(STATIC_ROOT)
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8888'))
    except ValueError:
        PORT = 8888

    @bottle.route('/static/<filepath:path>')
    # 处理服务器端静态文件
    def server_static(filepath):
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(server='wsgiref', host=HOST, port=PORT)
