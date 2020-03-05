from .recommend import Recommendations
import sqlite3
import psycopg2
import pandas as pd
rec = Recommendations()

rec.connect(psycopg2.connect("postgres://hbxxvjdj:WKiU7AFZ_NQlwT1D0EQWStM1EwUqOg4K@rajje.db.elephantsql.com:5432/hbxxvjdj"))

df = pd.read_csv('./SpotifyTracks_doubleforloop_genre_year_onehots.csv', index_col=[0])

song = df.iloc[0, 7:]
recs = rec.recommend(song)
print(recs)