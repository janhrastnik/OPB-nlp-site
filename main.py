from bottle import run, route, template, get
from bottle import TEMPLATE_PATH
from Services.sighting_service import SightingService
from Data.db_setup import DatabaseSetup

TEMPLATE_PATH.append('./Presentation/views')

sighting_service = SightingService()
database_setup = DatabaseSetup()

@route('/hello')
def hello():
    return template('home.html')


@route('/profil')
def profil():
    return template('profil.html')

@route('/api')
def profil():
    return template('api.html')

@get('/get_all_sightings')
def get_all_sightings():
    sighting_service.get_all_sightings()

if __name__ == '__main__':
    # TODO: use sys.argv to enable user to force a clean setup
    if database_setup.should_setup():
        database_setup.setup()
    run(host='localhost', port = 8080, debug=True)

