import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle

class Recommendations:
    '''Recommendation engine that uses NearestNeighbors model and Spotify API to return recommend songs'''
    def __init__(self):
        pass

    def connect(connection):
        '''Establish SQL connection and cursor'''
        self.conn = connection
        self.cursor = self.conn.cursor()
        
    def recommend(track_array):
        '''Use model and SQL queries to recommend songs
        Parameters:
        track_array (pandas Series): array of song traits for input into model 
        Returns:
        recommendations (str, str, str, int, int, str, int, int, int, int, int):  of song
        '''
        model = pickle.load(open('knn.pkl', 'rb'))
#         #Query DB for input's track ID
#         query = f'''
#         SELECT popularity, danceability, energy, key, loudness,
#         mode, speechiness, acousticness, instrumentalness, liveness,
#         valence, tempo, duration_ms, time_signature
#         FROM SpotifyData
#         WHERE track_id='{track_id}'
#         '''
#         curs.execute(query)
#         obs = curs.fetchone()
        #Reshape song's attributes to list
        song = track_array.to_numpy().reshape(1, -1)
        neighbors = model.kneighbors(song)
        #Return the 5th to 20th
        new_obs = neighbors[1][0][5:20]
        #Query list of recommended songs and their attributes
        query = f'''
        SELECT * FROM SpotifyData
        WHERE id IN {tuple(new_obs)}
        '''
        curs.execute(query)
        recommendations = curs.fetchall()
        conn.close()
        return recommendations