import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from decouple import config

from .dummy_functions import get_ten_tracks
from .spotify_functions import get_base_song_vector
from .prediction import make_genre_vector, get_genre, augment_song_vector

def create_app():
    app = Flask(__name__)
    CORS(app)


    app.config['ENV'] = config('ENV')


    # testing NN prediction here
    print(augment_song_vector(get_base_song_vector('3AJwUDP919kvQ9QcozQPxg')))


    # three routes
    # /by_track_id : takes a set of track ids (including a set of one!), returns ten recommendations
    # I'm thinking this can be used for favorites as well, if "favorites" just ends up being a set of track ids?
    @app.route('/by_track_id', methods=['POST'])
    def by_track_id():
        """takes a set of track ids (including a set of one!), returns ten recommendations."""

        #content = request.get_json(force=True)

        ten_track_df = get_ten_tracks()

        tuples = [item for item in ten_track_df.itertuples(index=False)]

        labels = ['artist_name', 'track_name', 'track_id', 'genre', 'danceability_diff', 'energy_diff',
       'loudness_diff', 'mode', 'speechiness_diff', 'acousticness_diff', 'instrumentalness_diff',
       'liveness_diff', 'valence_diff', 'tempo_diff']

        tupledicts = [dict(zip(labels,tuple)) for tuple in tuples]

        return json.dumps(tupledicts)


        

    # /by_custom_input : takes a feature vector, returns ten recommendations
    @app.route('/by_custom_input', methods=['POST'])
    def by_custom_input():
        """takes a set of track ids (including a set of one!), returns ten recommendations."""

        #content = request.get_json(force=True)

        ten_track_df = get_ten_tracks()

        tuples = [item for item in ten_track_df.itertuples(index=False)]

        labels = ['artist_name', 'track_name', 'track_id', 'genre', 'danceability_diff', 'energy_diff',
       'loudness_diff', 'mode', 'speechiness_diff', 'acousticness_diff', 'instrumentalness_diff',
       'liveness_diff', 'valence_diff', 'tempo_diff']

        tupledicts = [dict(zip(labels,tuple)) for tuple in tuples]

        return json.dumps(tupledicts)



    return app