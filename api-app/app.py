from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlite3

app = Flask(__name__)

#Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify_tracks.sqlite3'
DB = SQLAlchemy(app)
spotify_tracks_tbl = db.Table('songs', db.metadata, autoload=True, autoload_with = db.engine)
songs = db.session.query(spotify_tracks_tbl).all()

#convert dataframe into db

df = pd.read_csv('SpotifyData/SpotifyData.csv.zip')
conn = sqlite3.connect('spotify_tracks.sqlite3')
df.to_sql('songs',conn, if_exists='replace')



@app.route('/')
def home():
    # return some basic template with render_template 