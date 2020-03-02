from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sklearn
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np


df = pd.read_csv('https://github.com/spotify-song-suggester-1/DS-API/blob/master/sample_data.csv')

def process_input(song_id, return_json=True):
    c = ["duration_ms", "index", "genre","artist_name","track_name","track_id","key","mode"] #omitted columns
    song = df[df["track_id"] == song_id].iloc[0] #get song
    df_selected  =df.copy()
    if not pd.isnull(song["genre"]): #if genre, set subset to only genre
        df_selected = df[df["genre"] == song["genre"]]
    nn = NearestNeighbors(n_neighbors = 11, algorithm="kd_tree") #nearest neighbor model
    nn.fit(df_selected.drop(columns=c))
    song = song.drop(index=c)
    song = np.array(song).reshape(1,-1)
    if return_json is False:
        return df_selected.iloc[nn.kneighbors(song)[1][0][1:]]# return results as df
    return df_selected.iloc[nn.kneighbors(song)[1][0][1:]].to_json(orient="records") #returns results as json

    app = Flask(__name__)

    @app.route('/song/<song_id>', methods=['GET'])
    def song(song_id):
        "Route for recommendations based on song selected."""
        return process_input(song_id) #jsonified recommendations
    
    @app.route('/favorites', methods = ['GET','POST'])
    def favorites():
        my_dict  =request.get_json(force=True)
        track_list = pd.DataFrame()
        for i in my_dict.values():
            track_list = track_list.append(process_input(i, False))
        track_list.drop_duplicates()
        return track_list.sample(10).to_json(oreint="records")

