from functools import wraps
from bottle import run, route, template, get, post, request, hook, delete
from bottle import TEMPLATE_PATH, response, redirect, url, static_file
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

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    Prirejeno iz: https://github.com/gasperxy/opb-struktura-projekta 
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("user")
        if cookie and cookie != "":
            return f(*args, **kwargs)
        redirect(url('/login'))
        
    return decorated

@hook('before_request')
def cookies_check():
    # if a user cookie exists, then the user is logged in
    # the cookies value is the users email
    user_cookie = request.get_cookie('user')

    global email
    email = user_cookie

@route('/')
def index():
    return custom_template('index.html')

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@route('/profil')
@cookie_required
def profil():
    # TODO: get rest of needed user info from cookie
    user_cookie = request.get_cookie('user')

    user = user_service.get_user(user_cookie)
    sightings = sighting_service.get_user_sightings(user_cookie)
    
    return custom_template('profil.html', sightings=sightings, username=user.username)

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

    sightings = sighting_service.get_sightings_paginated(page)
    
    return custom_template('all_sightings.html', page=page, sightings=sightings)


@route('/add_sighting')
@cookie_required
def add_sighting():
    return custom_template('add_sighting.html')


@post('/do_add_sighting')
@cookie_required
def do_add_sighting():
    #print(dict(request.forms))
    timestamp = request.forms.get('user_timestamp')
    city = request.forms.get('city')
    state = request.forms.get('state')
    country = request.forms.get('country')
    shape = request.forms.get('shape')
    duration_seconds = float(request.forms.get('duration_seconds') or 0)
    comment = request.forms.get('comment')
    latitude = float(request.forms.get('latitude') or 0)
    langtitude = float(request.forms.get('langtitude') or 0)

    user_cookie = request.get_cookie('user')

    sighting_service.add_sighting(
        user_cookie,
        timestamp,
        city,
        state,
        country,
        shape,
        duration_seconds,
        comment,
        latitude,
        langtitude
    )

    return redirect('/profil')

@route('/sighting/<sighting_id>')
def view_sighting(sighting_id):

    sighting = sighting_service.get_sighting_by_id(sighting_id)

    comments = sighting_service.get_sighting_comments(sighting_id)
    
    return custom_template('sighting.html', sighting=sighting, comments=comments)

@post('/do_add_comment')
@cookie_required
def do_add_comment():
    comment = request.forms.get('comment')
    sighting_id = int(request.forms.get('sighting_id'))

    user_cookie = request.get_cookie('user')

    user_service.add_comment(email, comment, sighting_id)

    redirect(f'/sighting/{sighting_id}')


@delete('/sighting/<sighting_id:int>')
@cookie_required
def delete_sighting(sighting_id):
    user_email = request.get_cookie('user')
    success = sighting_service.delete_sighting(sighting_id, user_email)
    if success:
        response.status = 200
        return {'success': True}
    else:
        response.status = 404
        return {'error': 'Sighting not found or not yours'}


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
