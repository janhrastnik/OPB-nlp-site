from bottle import run, route, template, Bottle
from bottle import TEMPLATE_PATH

TEMPLATE_PATH.append('./Presentation/views')

@route('/hello')
def hello():
    return template('home.html')

if __name__ == '__main__':
    run(host='localhost', port = 8080, debug=True)

