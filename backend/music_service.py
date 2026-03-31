import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='a',
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

class MusicService:
    def __init__(self, sp):
        self.sp = sp

    def get_music_data(self): #i need to call this function when session is active, every 30-60 sec.
        try:
            current_track = self.sp.current_user_playing_track()

            if current_track is not None and current_track['is_playing']:
                current_track_name = current_track['item']['name']
                current_track_artist = current_track['item']['artists'][0]['name']
                current_track_album = current_track['item']['album']['name']

                #spotify got rid of genres - weird behaviour ngl, gatekeeping genres.

                #current_track_artist_id = current_track['item']['artists'][0]['id']
                #current_artist = self.sp.artist(current_track_artist_id)
                #current_track_genre = current_artist.get('genres', []) #this can return multiple genre btw, its any genre the artist is associated with.

                return f"{current_track_name}${current_track_artist}${current_track_album}"
            
            print("Spotify connected, but no active track found.")
            return None
        except Exception as e:
            logging.error(f"Spotipy API Error: {e}")
            return None
        
