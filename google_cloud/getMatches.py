#!/usr/bin/env python3

import json  
from pprint import pprint 
from scipy import spatial

# API Client Library
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yelpapi import YelpAPI
from tmdbv3api import TMDb, Movie, Genre, Discover

# Firebase Libraries
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


'''
Requirements.txt:
scipy
tmdbv3api
spotipy
yelpapi
firebase-admin
'''

# SECRETS

SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET = ''
YELP_KEY = ''
TMDB_KEY= ''

# Spotipy client
auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Yelp client
yelp_api = YelpAPI(YELP_KEY)

# TMDB client
tmdb = TMDb()
tmdb.api_key = TMDB_KEY 

# Firestore client
# Setup firestore creds
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': ''
    })
db = firestore.client()


# Preference Vector
'''
First is E or I
Second is music
Third is Movies
Fourth is Food
Score is out of 100
'''
achoo = {
        "username": "achoo", 
        "preferences": [100, 0, 0, 100]
        }

# Debugging
API_DEBUG = True

# API Helpers
def genre_builder():
    genre_mapping = {}
    genre = Genre()
    genres = genre.movie_list()
    for g in genres:
        # Sanitize name
        name = (g.name).lower()
        genre_mapping[name] = g.id
    return genre_mapping

# API callers
# TMDB caller
def TMDB_rec(genre='action'):
    genre_map = genre_builder()

    # Sanity check
    if genre not in genre_map:
        genre = 'action'

    discovery = Discover()
    movie = discovery.discover_movies({
        'sort_by': 'popularity.desc',
        'with_genres': genre_map[genre]
    })
    movie_rec = movie[0]

    movie_json = {
        "movie": {
            "title" : movie[0]['original_title'],
            "rating": int(float(movie[0]['vote_average'])/2),
            "summary": movie[0]['overview'],
            "genre":genre
        }
    }

    if API_DEBUG:
        print(movie_json)
    
    return movie_json

# Queries Yelp API given string and location
# Returns a tuple of Name and URL of business
def yelp_rec(food='ice cream', user_loc='toronto, on'):
    yelp_resp = yelp_api.search_query(term=food, location=user_loc, sort_by='rating', limit=1)

    business = yelp_resp['businesses'][0]

    if API_DEBUG:
        print(business['name'], business['url'])

    yelp_json = {
        "food":{
            "phone": business['display_phone'],
            "restaurant":business['name'],
            "url":business['url'],
            "genre": food
        }
    }

    return yelp_json

def spotify_rec(music='classical'):
    spotify_resp = sp.search(music, 1, 0, 'playlist', None)

    # Parse the response to get uri
    uri = spotify_resp['playlists']['items'][0]['uri']
    if API_DEBUG:
        print(spotify_resp['playlists']['items'][0]['name'])

    spotify_json = {
        "playlist":{
            "spotify_uri": uri,
            "genre": music
        }
    }

    return spotify_json

def game_rec(game='Minecraft'):
    game_res = {
        "game": {
            "name":"Minecraft"
        }
    }
    return game_res

# Return Date Plans
def date_planner(music='classical', food='ice cream', user_loc='toronto, on', movie_genre='action'):
    spotify_uri = spotify_rec(music)
    yelp_res = yelp_rec(food, user_loc)
    movie_res = TMDB_rec(movie_genre)
    game_res = game_rec()

    result_json = {**spotify_uri, **yelp_res, **movie_res, **game_res}

    return result_json

# Returns a JSON payload for testing
def mock_request():
    response = {
        "username": "achoo", 
        "location": "toronto, ca",
        "mbti": "intj",
        "music": ["kpop"],
        "movies": ["comedy"],
        "food": ["american"],
        }
    t2 = {
        "username": "ched", 
        "location": "toronto, ca",
        "mbti": "entp",
        "music": ["folk"],
        "movies": ["action"],
        "food": ["sushi"],
        }
    return response

# Hard coded profiles in a list
def get_profiles():
    # INFP 
    Alice = {
        "username": "alice", 
        "preferences": [100, 30, 10, 70]
        }
    Bob = {
        "username": "bob", 
        "preferences": [0, 20, 10, 15]
        }
    return [Alice, Bob]

def get_match(userid):
    matches_ref = db.collection(u'matches').document(userid)
    matches = matches_ref.get()
    match_list = matches.get('matches')

    print(matches)

    profile_ref = db.collection(u'users').document(match_list[0])
    match_profile = profile_ref.get()
    return match_profile

# From user response, calculate the preference vector
def calculate_preferences(user):
    return {
        "username": "achoo", 
        "preferences": [100, 0, 0, 100]
        }

# Returns string of user name
def match_profile(user, profiles):
    user_preferences = user['preferences']
    min_dist = 1_000_000
    match = None
    # Use a KNN algorithm to determine the smallest pairwise distance to find match
    for p in profiles:
        dist = spatial.distance.euclidean(user_preferences, p['preferences'])
        if dist < min_dist:
            min_dist = dist
            match = p['username']
    return match

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
    data = request.get_json()

    print("REQUEST :" , data)

    match_profile = get_match(data['username'])
    print(match_profile.to_dict())

    date_plan = date_plan = date_planner(data["music"][0], data['food'][0], data['location'], data['movies'][0])

    result = {
        "hangout": date_plan,
        "match_profile": match_profile.to_dict()
    }

    return (result, 200, headers)

# Sample req
'''
curl  -d '{"username":"ched","location":"toronto,ca","mbti":"entp","music":["folk"],"movies":["action"],"food":["sushi"]}' -H 'Content-Type: application/json' 'https://us-west2-uofthack21.cloudfunctions.net/simple-res'
curl  -d '{"username":"achoo2","location":"toronto,ca","mbti":"entp","music":["folk"],"movies":["action"],"food":["sushi"]}' -H 'Content-Type: application/json' 'https://us-west2-uofthack21.cloudfunctions.net/get_recs'
curl  -d '{"username":"ched","location":"toronto,ca","mbti":"entp","music":["folk"],"movies":["action"],"food":["sushi"]}' -H 'Content-Type: application/json' 'https://us-east4-uofthacks-matching.cloudfunctions.net/getMatches'
curl  -d '{"username":"turbo","profile":{"first_name":"Achoo","last_name":"Hamtaro","gender":"male","age":24,"mbti":"INTJ","location":"Toronto,Canada","loc_preference":"virtual","movies":["Action","Thriller","Horror"],"music":["Folk","Classical"],"food":["American","French"],"games":["LeagueofLegends","Minecraft","RocketLeague"]}}' -H 'Content-Type: application/json' 'https://us-central1-uofthack21.cloudfunctions.net/create-user'
'''