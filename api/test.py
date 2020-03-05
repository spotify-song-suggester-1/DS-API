from recommend import Recommendations
from spotify_functions import query_spotify, get_base_song_vector
from prediction import augment_song_vector
import sqlite3
import psycopg2
import pandas as pd
rec = Recommendations()

rec.connect(psycopg2.connect("postgres://hbxxvjdj:WKiU7AFZ_NQlwT1D0EQWStM1EwUqOg4K@rajje.db.elephantsql.com:5432/hbxxvjdj"))

# df = pd.read_csv('./SpotifyTracks_doubleforloop_genre_year_onehots.csv', index_col=[0])

# song = df.iloc[0, 7:]
# recs = rec.recommend(song)
# print(recs)
query = query_spotify('i am the walrus')
vector = get_base_song_vector(query[0]['track_id'])
augmented = augment_song_vector(vector)

print(rec.recommend(augmented))
