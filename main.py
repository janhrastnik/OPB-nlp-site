from bottle import run, route, template
from bottle import TEMPLATE_PATH

TEMPLATE_PATH.append('./Presentation/views')


@route('/hello')
def hello():
    return template('home.html')


@route('/profil')
def profil():
    return template('profil.html')

@route('/login')
def login():
    return template('login.html')

@route('/register')
def register():
    return template('register.html')



if __name__ == '__main__':
    run(host='localhost', port = 8080, debug=True)

