from bottle import run,request, route,template
from bottle import get, post, request # or route
from bottle import error

# 报错信息
@error(404)
def error404(error):
	return '404 not find'
#简易表单	
@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if True:
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
'''
@route('/hello')
def hello():
	return "Hello World"
'''

# 调用html文件
@route('/', methods=['GET','POST'])
def hello_world():
    return template('index.html')

@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@route('/object/<id:int>')
def callback(id):
    assert isinstance(id, int)
    print("in this")

@route('/show/<name:re:[a-z]+>')
def callback(name):
    assert name.isalpha()
    print("in that")

@route('/static/<path:path>')
def callback(path):
    return static_file(path, ...)

run(host='0.0.0.0',port=8080,debug=True)