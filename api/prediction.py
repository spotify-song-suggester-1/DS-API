"""Functions for genre inference using the tensorflow model, and recommendation inference using the KNN model."""

import tensorflow as tf
import pandas as pd
import joblib

from .spotify_functions import get_base_song_vector

genre_inference_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key','liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
genre_list = ['alternative', 'country', 'dance', 'folk', 'grunge', 'indie', 'jazz', 'metal', 'pop', 'punk', 'rap', 'rock']
genre_onehot_labels = ['genre_' + x for x in genre_list]

genre_NN = tf.keras.models.load_model('../genre_NN')
genre_NN._make_predict_function()
scaler = joblib.load('../genre_NN_scaler')


def make_genre_vector(song_vector):
    """takes a song vector and returns the onehot genre prediction for the song."""

    feature_vector = song_vector[genre_inference_features].copy().to_numpy()

    scaled_vector = scaler.transform(feature_vector.reshape(1,-1))

    genre_vector = genre_NN.predict(scaled_vector)

    return genre_vector


def get_genre(genre_vector):
    """takes a genre vector and returns the appropriate genre as a string."""
    vector_list = genre_vector.tolist()[0]
    best_tuple =  sorted(zip(vector_list, genre_list), reverse=True)[0]
    best_genre = best_tuple[1]
    return best_genre


def augment_song_vector(song_vector):
    """takes a song vector and adds a genre string and onehot genre features."""

    song_vector_output = song_vector.copy()
    genre_vector = make_genre_vector(song_vector)

    song_vector_output['genre'] = get_genre(genre_vector)

    genre_dict = dict(zip(genre_onehot_labels,genre_vector.tolist()[0]))

    genre_series = pd.Series(genre_dict)

    song_vector_output = pd.concat([song_vector_output, genre_series])

    return song_vector_output