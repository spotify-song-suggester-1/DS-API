''' Retrieve data, Functions, embedding, save into db (ETL)'''import basilica
import spotipy
from decouple import config
from .models import DB
from os import getenv