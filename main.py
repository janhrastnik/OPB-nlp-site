from bottle import run, route, template, get, post, request, hook
from bottle import TEMPLATE_PATH, response, redirect, url
from Services.sighting_service import SightingService
from Data.db_setup import DatabaseSetup
from Services.user_service import UserService
import sys

TEMPLATE_PATH.append('./Presentation/views')

sighting_service = SightingService()
user_service = UserService()
database_setup = DatabaseSetup()

email = None

def custom_template(template_name, **kwargs):
    return template(template_name, email=email, **kwargs)

@hook('before_request')
def cookies_check():
    # if a user cookie exists, then the user is logged in
    # the cookies value is the users email
    user_cookie = request.get_cookie('user')

    email = user_cookie

@route('/hello')
def hello():
    return custom_template('home.html')

@route('/')
def index():
    return custom_template('index.html')

@route('/profil')
def profil():
    # TODO: get rest of needed user info from cookie

    return custom_template('profil.html')

@route('/login')
def login():
    return custom_template('login.html')

@post('/do_login')
def do_login():
    email = request.forms.email
    password = request.forms.password
    
    if not user_service.user_exists(email):
        print("USER DOES NOT EXIST IN DATABASE")
        # user isn't registered
        # TODO: tell user this email isn't registered
        redirect(url('/register'))
    else:
        login_res = user_service.login(email, password)

        if login_res:
            # login succeeded
            # TODO: maybe setup cookies in a safer way
            response.set_cookie('user', email)
    
        redirect(url('/profil'))
        #return template('profil.html')

@route('/register')
def register():
    return custom_template('register.html')

@post('/do_register')
def do_register():
    email = request.forms.email
    nickname = request.forms.nickname
    password = request.forms.password

    user_service.register_user(email, nickname, password)

    # if successful, redirect to login
    redirect(url('/login'))
    #return template('login.html')

@post('/logout')
def do_logout():
    response.delete_cookie('user')
    redirect(url('/'))


@route('/api')
def api():
    return custom_template('api.html')

@get('/get_all_sightings')
def get_all_sightings():
    res = sighting_service.get_all_sightings()
    result = str(res)
    response.content_type = 'text/plain'
    return result

@get('/get_all_users')
def get_all_users():
    user_service.get_all_users()

@route('/all_sightings')
def all_sightings():

    page = 1
    query = request.query_string

    if query.startswith("page="):
        try:
            page = int(query[5:])
        except ValueError:
            # query parameter is wrong, just redirect user back to original page
            redirect(url('/all_sightings'))
    
    print(page)
    
    return custom_template('all_sightings.html')

@route('/add_sighting')
def add_sighting():
    return custom_template('add_sighting.html')

if __name__ == '__main__':
    clean_install_flag = False
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--clean":
            clean_install_flag = True

    if database_setup.should_setup() or clean_install_flag:
        print("SETTING UP THE DATABASE")
        database_setup.setup()

    run(host='localhost', port = 8080, debug=True)

