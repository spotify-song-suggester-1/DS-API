"""  Main application for Spotify Flask App """


from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import db
# from .suggest import suggest_songs
# from os import getenv

load_dotenv()

def create_app():
    '''Create and configure an instance of the flask app'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify_tracks.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['ENV'] = getenv('FLASK_ENV')
    db.init_app(app)

    @app.route('/')
    def home():
        return("Good Start Krista")