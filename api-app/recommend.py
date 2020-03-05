import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle

class Recommendations:
    '''Recommendation engine that uses NearestNeighbors model and Spotify API to return recommend songs'''
    def __init__(self):
        self.model = pickle.load(open('knn.pkl', 'rb'))

    def connect(connection):
        '''Establish SQL connection and cursor'''
        self.conn = connection
        self.cursor = self.conn.cursor()

    def recommend(self, track_array):
        '''Use model and SQL queries to recommend songs
        
        Parameters:
        track_array (pandas Series): array of song traits for input into model 
        
        Returns:
        recommendations (str, str, str, int, int, str, int, int, int, int, int):  of song
        
        '''
        #Reshape song's attributes to list
        song = track_array.to_numpy().reshape(1, -1)
        neighbors = self.model.kneighbors(song)
        #Return the 5th to 20th
        new_obs = neighbors[1][0][0:9]
        #Query list of recommended songs and their attributes
        query = f'''
        SELECT * FROM SpotifyData
        WHERE id IN {tuple(new_obs)}
        '''
        self.cursor.execute(query)
        recommendations = self.cursor.fetchall()
        self.conn.close()
        return recommendations