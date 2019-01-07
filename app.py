"""Flask App Project."""

import string
import random
from flask import Flask, jsonify, request, json, send_file
from random import randint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100000 per day", "50000 per hour"]
)

usernames = {}
words_with_two_letters = ['ga', 'go', 'do', 'ja', 'ma', 'pa', 'te', 'of', 'mi', 'we', 'ze', 'zo']
most_often_used_passwords = [
    123456, '123456', 'password', 12345678, "12345678", "qwerty", 12345, 123456789, "123456789",
    'letmein', 1234567, '1234567', 'football', 'iloveyou', 'admin', 'welcome', 'monkey', 'login',
    'abc123','starwars',123123,'123123','dragon','passw0rd','master','hello','freedom','whatever',
    'qazwsx','trustno1'
]

def check_password(endpoint, username, password):
    if usernames[username][endpoint] == password:
        return True
    else:
        return False

def find_or_create_user(username):
    if username not in usernames.keys():
        usernames[username] = { 
            'login1': randint(0, 9), 
            'login190837': randint(0, 999), 
            'login467890': random.choice(string.ascii_lowercase),
            'login0abcde': random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase),
            'login_dictionary_2_letters': random.choice(words_with_two_letters),
            'login_dictionary_veel_gebruikte_wachtwoorden': random.choice(most_often_used_passwords),
            'supersafe': 409,
        }

def handle_error(body):
    if 'password' not in body.keys() and 'username' not in body.keys():
        return 'Geen password en username in de data van je request, sorry', 400

    if 'password' not in body.keys():
        return 'Geen password in de data van je request, sorry', 400
    
    if 'username' not in body.keys():
        return 'Geen username in de data van je request, sorry', 400

    return 'All is OK'

def create_response(data, endpoint, next_url, instructions):

    if data == b'':
        return 'Je request heeft geen data, sorry', 400

    dataDict = json.loads(data)

    if handle_error(dataDict) != 'All is OK':
        return handle_error(dataDict)

    password = dataDict['password']
    username = dataDict['username']

    find_or_create_user(username)

    response = { 'username': username, 'password': password }

    response['correct'] = check_password(endpoint, username, password)

    if response['correct']:
        if next_url == 'https://github.com/Reinoptland/hacking-workshop/blob/master/app.py':
            response['next_url'] = 'https://github.com/Reinoptland/hacking-workshop/blob/master/app.py'
        else:
            response['next_url'] = 'ministerie-van-geheime-zaken' + next_url
            response['instructies'] = instructions

    return jsonify(response)


@app.route('/')
def index():
    """Return homepage."""
    json_data = {'Hello': 'World!'}
    return jsonify(json_data)

@app.route('/brute_force/login1', methods=['POST'])
def brute_force_1():
    response = create_response(request.data, 'login1', '/brute_force/login190837', 'De volgende url heeft password tussen 0 en 999, hint: gebruik een for loop')
    return response

@app.route('/brute_force/login190837', methods=['POST'])
def brute_force_2():
    response = create_response(request.data, 'login190837', '/brute_force/login467890', 'De volgende url heeft een password van een kleine letter bijvoorbeeld `a` hint: maak een Array (of een list) van letters: [`a`, `b`] en gebruik die in je for loop')
    return response

@app.route('/brute_force/login467890', methods=['POST'])
def brute_force_3():
    response = create_response(request.data, 'login467890', '/dictionary/login_dictionary_2_letters', 'Het password van de volgend url is twee letterwoord uit het nederlandse woordenboek')
    return response

@app.route('/dictionary/login_dictionary_2_letters', methods=['POST'])
def dictionary_1():
    response = create_response(request.data, 'login_dictionary_2_letters', '/dictionary/login_dictionary_veel_gebruikte_wachtwoorden', 'De volgende url heeft een password dat in de top 50 staat van meest gebruikte wachtwoorden, maak een dictionary door te zoeken op internet')
    return response

@app.route('/dictionary/login_dictionary_veel_gebruikte_wachtwoorden', methods=['POST'])
def dictionary_2():
    response = create_response(request.data, 'login_dictionary_veel_gebruikte_wachtwoorden', '/brute_force/login0abcde', 'De volgende url heeft een password van TWEE kleine letters bijvoorbeeld `aa` of `ab` of `ac` ')
    return response

@app.route('/brute_force/login0abcde', methods=['POST'])
def brute_force_4():
    response = create_response(request.data, 'login0abcde', 'NO NEXT_URL YOU`RE THE MASTER HACKERRR, CONGRATZ', 'Celebrate!!')
    return response

@app.route('/supersafe', methods=['POST'])
@limiter.limit("3 per hour")
def supersafe():
    response = create_response(request.data, 'supersafe', '/dictionary/login_dictionary_veel_gebruikte_wachtwoorden')
    
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    
    return response


@app.route('/loaderio-3837a25d23b03c414d981afd578e2059/', methods=['GET'])
def loaderio():
    return send_file('loaderio-3837a25d23b03c414d981afd578e2059.txt')


if __name__ == '__main__':
    app.run()
