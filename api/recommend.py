import sqlite3
import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
class Recommendations:
    '''Recommendation engine that uses NearestNeighbors model and Spotify API to return recommend songs'''
    def __init__(self):
        self.model = joblib.load(open('knn.pkl', 'rb'))
    def connect(self, connection):
        '''Establish SQL connection and cursor'''
        self.conn = connection
        self.cursor = self.conn.cursor()
    def recommend(self, track_array):
        '''Use model and SQL queries to recommend songs
        
        Parameters:
        track_array (pandas Series): array of song traits for input into model 
        
        Returns:
        recommendations (list of dicts):  of song
        
        '''
        #Reshape song's attributes to list
        track_array = track_array[5:].drop(labels='genre', axis=0)
        song = track_array.to_numpy().reshape(1, -1)
        neighbors = self.model.kneighbors(song)
        #Return the 5th to 20th
        new_obs = neighbors[1][0][0:9]
        #Query list of recommended songs and their attributes
        query = f'''
        SELECT * FROM "SpotifyTracks"
        WHERE id IN {tuple(new_obs)}
        '''
        self.cursor.execute(query)
        tuples = self.cursor.fetchall()
        self.conn.close()
        #Transform list of tuples into dictionary
        recommendations = []
        attributes = ['artist_name', 'track_name', 'track_id', 'popularity', 'year', 'genre',
       'id', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
       'speechiness', 'tempo', 'time_signature', 'valence']
        for song in tuples:
                #Convert each tuple to list
                song = list(song)
                #Append dictionary of song values to recommendations list
                recommendations.append(dict(zip(attributes, song)))
                
        return recommendations