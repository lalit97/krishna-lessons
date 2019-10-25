import sys
import requests
from config import conf
from random import randrange


CLIENT_ID = conf['gita_api']['CLIENT_ID']
CLIENT_SECRET = conf['gita_api']['CLIENT_SECRET']
BASE_URL = 'https://bhagavadgita.io/'
VERSE_COUNT = {
    '1': 47,
    '2': 72,
    '3': 43,
    '4': 42,
    '5': 29,
    '6': 47,
    '7': 30,
    '8': 28,
    '9': 34,
    '10': 42,
    '11': 55,
    '12': 20,
    '13': 35,
    '14': 27,
    '15': 20,
    '16': 24,
    '17': 28,
    '18': 78
}


def get_json_response(response):
    ''' Convert HttpResponse into Json format'''
    try:
        response = response.json()
    except ValueError as e:
        sys.exit('Cannot Convert Response To Json')
    return response


def post_response(url, headers=None, data=None):
    ''' Make Post request based on given headers'''
    try:
        response = requests.post(url, headers=headers, data=data)
    except requests.exceptions.RequestException as e:
        sys.exit('Enter Valid Url')
    response = get_json_response(response)
    return response


def get_response(url, params=None):
    ''' Make Get request with given params'''
    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        sys.exit('Enter Valid Url')
    response = get_json_response(response)
    return response


def get_chap_verse():
    ''' Get a random chapter and verse number'''
    chap_num = randrange(1, 18)
    verse_count = VERSE_COUNT.get(str(chap_num))
    if not verse_count:
        sys.exit('Invalid Verse Number')
    verse_num = randrange(1, verse_count)
    url_str = f'chapters/{chap_num}/verses/{verse_num}'
    return url_str


def get_access_token():
    ''' Get access_token to access API'''
    add_on = 'auth/oauth/token'
    url = BASE_URL + add_on
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'verse chapter'
    }
    response = post_response(url, headers=headers, data=data)
    access_token = response.get('access_token')
    if not access_token:
        sys.exit('Access Not Found')
    return access_token


def get_data(access_token, chap_verse, language=None):
    ''' Get requested verse'''
    add_on = 'api/v1/'
    url = BASE_URL + add_on + chap_verse
    params = {
        'access_token': access_token
    }
    if language:
        params['language'] = language
    response = get_response(url, params)
    return response


def get_text(response):
    ''' Extract text from response'''
    chapter = response.get('chapter_number')
    verse = response.get('verse_number')
    text = response.get('text')
    if not chapter or not verse or not text:
        sys.exit('Key Names Are Incorrect')
    return f'chapter {chapter}, verse {verse}\n{text}'


def get_meaning(response):
    ''' Extract meaning from response'''
    meaning = response.get('meaning')
    if not meaning:
        sys.exit('Meaning Not Found')
    return meaning
