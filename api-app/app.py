"""  Main application for Spotify Flask App """

from decouple import config
#from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import getenv

from .dummy_functions import get_ten_tracks
from .spotify_functions import get_base_song_vector, query_spotify, get_album_art
from .prediction import make_genre_vector, get_genre, augment_song_vector

import json
import pandas as pd
import numpy as np
import urllib


DB = SQLAlchemy()

# Make app factory
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify_tracks.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    CORS(app)

    # DB.init_app(app)

    # conn = sqlite3.connect('spotify_tracks.sqlite3')

    @app.route("/")
    def root():
        return render_template('base.html', title='Home')

    @app.route('/testpath/<track_id>')
    def testpath(track_id):
        """Using this to test prediction functions."""
        vec = augment_song_vector(get_base_song_vector(track_id))

        labels = list(vec.index)
        values = list(vec.values)

        output = dict(zip(labels,values))
        return output

    # three routes
    # /by_track_id : takes a set of track ids (including a set of one!), returns ten recommendations

    # I'm thinking this can be used for favorites as well, if "favorites" just ends up being a set of
    # track ids?

    @app.route('/by_track_id/<track_id>')
    def by_track_id(track_id):
        """takes a set of track ids (including a set of one!), returns ten recommendations."""

        #content = request.get_json(force=True)

        ten_track_df = get_ten_tracks()

        tuples = [item for item in ten_track_df.itertuples(index=False)]

        labels = ['artist_name', 'track_name', 'track_id', 'genre', 'danceability_diff', 'energy_diff',
       'loudness_diff', 'mode', 'speechiness_diff', 'acousticness_diff', 'instrumentalness_diff',
       'liveness_diff', 'valence_diff', 'tempo_diff']

        tupledicts = [dict(zip(labels,tuple)) for tuple in tuples]

        return json.dumps(tupledicts)

        # /search query
    @app.route('/query/<query_string>')
    def query(query_string):
        res = query_spotify(urllib.parse.unquote(query_string))
        return jsonify(res)


    @app.route('/recommend/<track_id>')
    def recommend(track_id):
        """Using this to test prediction functions."""
        vec = augment_song_vector(get_base_song_vector(track_id))
        labels = list(vec.index)
        values = list(vec.values)
        output = dict(zip(labels,values))
        output['album_art'] = get_album_art(track_id)
        return jsonify([output]*10)

    return app