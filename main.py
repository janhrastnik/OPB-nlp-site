from bottle import run, route, template
from bottle import TEMPLATE_PATH

TEMPLATE_PATH.append('./Presentation/views')


@route('/hello')
def hello():
    return template('home.html')


@route('/profil')
def profil():
    return template('profil.html')


if __name__ == '__main__':
    run(host='localhost', port = 8080, debug=True)

