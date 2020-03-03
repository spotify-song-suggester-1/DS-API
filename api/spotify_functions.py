"""functions for accessing the spotify API and formatting the response."""

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


spotify = spotipy.Spotify(client_credentials_manager=credentials)

def get_base_song_vector(song_id):
    """takes a spotify track id, and returns the song as an array with the base features supplied by spotify."""
    # empty dict, will be dataframed
    non_feature_dict = {}

    # get non-feature data from the API
    non_feature_response = spotify.track(song_id)

    # put it in the dict
    non_feature_dict['artist_name'] = non_feature_response['artists'][0]['name']
    non_feature_dict['track_name'] = non_feature_response['name']
    non_feature_dict['track_id'] = non_feature_response['id']
    non_feature_dict['popularity'] = non_feature_response['popularity']
    non_feature_dict['year'] = int(non_feature_response['album']['release_date'][:4])

    # to pandas series
    non_feature_series = pd.Series(non_feature_dict)

    # get feature data from the API
    feature_response = spotify.audio_features(song_id)

    # to pandas series
    feature_series = pd.Series(feature_response[0])

    # reorder the series columns alphabetically
    cols = feature_series.axes[0]
    cols = sorted(cols)
    feature_series = feature_series[cols]

    """ # rename the id column
    feature_series.rename(index={'id': 'track_id'}, inplace=True)

    print(feature_series)"""

    # drop unused stuff
    stuff_to_drop = ['analysis_url','track_href','type','uri','id']
    feature_series.drop(stuff_to_drop, axis=0,inplace=True)

    # merge the data
    songseries = pd.concat([non_feature_series, feature_series])

    return songseries


