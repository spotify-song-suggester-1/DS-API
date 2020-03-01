"""functions for generating fake formatted output, for a dummy API."""

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

from decouple import config

import pandas as pd

SPOTIFY_CLIENT_ID = config('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = config('SPOTIFY_CLIENT_SECRET')

credentials = oauth2.SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

def get_ten_tracks():
    """gets ten tracks from the spotify API, in the format they'll be served to WEB."""

    artist_name = []
    track_name = []
    #popularity = []
    track_id = []

    track_results = spotify.search(q='year:2018 AND tag:hipster', limit=10, offset=0, market='US')

    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        #popularity.append(t['popularity'])

    df_tracks = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,'track_id':track_id})
    df_tracks['genre'] = 'placeholder'

    rows = []
    batchsize = 1
    None_counter = 0

    for i in range(0,len(df_tracks['track_id']),batchsize):
        batch = df_tracks['track_id'][i:i+batchsize]
        feature_results = spotify.audio_features(batch)
        for i, t in enumerate(feature_results):
            if t == None:
                None_counter = None_counter + 1
            else:
                rows.append(t)

    # create the audio features data frame.
    df_audio_features = pd.DataFrame.from_dict(rows,orient='columns')

    # rename id column to merge with tracks data frame.
    df_audio_features.rename(columns={'id': 'track_id'}, inplace=True)

    # drop useless columns.
    columns_to_drop = ['analysis_url','track_href','type','uri','key','duration_ms','time_signature']
    df_audio_features.drop(columns_to_drop, axis=1,inplace=True)

    # merge both dataframes with inner method to keep track IDs present in both data frames.
    df = pd.merge(df_tracks,df_audio_features,on='track_id',how='inner')

    return df