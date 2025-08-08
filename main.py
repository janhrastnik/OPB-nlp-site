from bottle import run, route, template, get, post, request
from bottle import TEMPLATE_PATH, response
from Services.sighting_service import SightingService
from Data.db_setup import DatabaseSetup
from Services.user_service import UserService
import sys

TEMPLATE_PATH.append('./Presentation/views')

sighting_service = SightingService()
user_service = UserService()
database_setup = DatabaseSetup()

@route('/hello')
def hello():
    return template('home.html')


@route('/profil')
def profil():
    return template('profil.html')

@route('/login')
def login():
    return template('login.html')

@post('/do_login')
def do_login():
    # TODO
    return template('profil.html')

@route('/register')
def register():
    return template('register.html')

@post('/do_register')
def do_register():
    email = request.forms.email
    nickname = request.forms.nickname
    password = request.forms.password

    user_service.register_user(email, nickname, password)
    # return template('login.html')

@route('/api')
def api():
    return template('api.html')

@get('/get_all_sightings')
def get_all_sightings():
    res = sighting_service.get_all_sightings()
    result = str(res)
    response.content_type = 'text/plain'
    return result

@get('/get_all_users')
def get_all_users():
    user_service.get_all_users()

@route('/add_sighting')
def add_sighting():
    return template('add_sighting.html')

if __name__ == '__main__':
    clean_install_flag = False
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--clean":
            clean_install_flag = True

    if database_setup.should_setup() or clean_install_flag:
        database_setup.setup()
    run(host='localhost', port = 8080, debug=True)

