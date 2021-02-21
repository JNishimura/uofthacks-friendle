import json
import firebase_admin
import constants
from firebase_admin import credentials
from firebase_admin import firestore

'''
Requirements.txt:
firebase-admin
'''


def mock_response():
    response = {}
    return response

def mock_request():
    request = {
        "username": "turbo",
        "profile": {
            "first_name": "Achoo",
            "last_name": "Hamtaro",
            "gender": "male",
            "age": 24,
            "mbti": "INTJ",
            "location": "Toronto, Canada",
            "loc_preference": "virtual",
            "movies": ["Action", "Thriller", "Horror"],
            "music": ["Folk", "Classical"],
            "food": ["American", "French"],
            "games": ["League of Legends", "Minecraft", "Rocket League"]
        }
    }

    return request

def profile_to_feature_vec(profile):
    weighted_vec = [0] * constants.VECTOR_LENGTH
    mbti_vec = [0] * constants.VECTOR_LENGTH

    mbti_type = profile['mbti']
    mbti_type = mbti_type.upper()
    mbti_compats = constants.MBTI_COMPATIBILITY[mbti_type]

    mbti_vec[constants.MBTI_TO_INDEX[mbti_type]] = 1

    for compat in mbti_compats['high']:
        weighted_vec[constants.MBTI_TO_INDEX[compat]] = 1
    for compat in mbti_compats['medium']:
        weighted_vec[constants.MBTI_TO_INDEX[compat]] = 0.66
    for compat in mbti_compats['low']:
        weighted_vec[constants.MBTI_TO_INDEX[compat]] = 0.33

    for food in profile['food']:
        food = food.upper()
        weighted_vec[constants.FOOD_TO_INDEX[food]] = 1
        mbti_vec[constants.FOOD_TO_INDEX[food]] = 1

    for movie in profile['movies']:
        movie = movie.upper()
        weighted_vec[constants.MOVIE_TO_INDEX[movie]] = 1
        mbti_vec[constants.MOVIE_TO_INDEX[movie]] = 1

    for game in profile['games']:
        game = game.upper()
        weighted_vec[constants.GAME_TO_INDEX[game]] = 1
        mbti_vec[constants.GAME_TO_INDEX[game]] = 1

    for music in profile['music']:
        music = music.upper()
        weighted_vec[constants.MUSIC_TO_INDEX[music]] = 1
        mbti_vec[constants.MUSIC_TO_INDEX[music]] = 1

    return (mbti_vec, weighted_vec)

def feature_vec_to_string(vec):
    return ''.join(map(str, vec))

# Take requests from the front end as JSON payload
# Entry method
def get_requests(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

     # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Setup firestore creds
    try:
        firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': ''
        })
    db = firestore.client()

    request_json = request.get_json()
    data = request_json 
    user_id = data['username']
    profile = data['profile']

    weighted_vec, mbti_vec = profile_to_feature_vec(profile)
    profile['weighted_vec'] = weighted_vec
    profile['mbti_vec'] = mbti_vec

    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.set(profile)

    # Add some matches until batch job occurs
    match_ref = db.collection(u'matches').document(user_id)
    achoo_match = {
        'matches': ['achoo', 'turbo', 'turbo25', 'achoo42']
    }

    match_ref.set(achoo_match)
    
    result = {}

    return (result, 200, headers)