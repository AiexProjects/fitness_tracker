import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='a',
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0e97f80b5b604237945e8b621f5b988e",
                                               client_secret="cb245b047475473293c152f40b6ffbc6",
                                               redirect_uri="https://localhost:3000",
                                               scope="user-library-read"))

class MusicService:
    def __init__(self, sp):
        self.sp = sp

    def get_music_data(self): #i need to call this function when session is active, every 30-60 sec.
        try:
            current_track = self.sp.current_user_playing_track()

            if current_track is not None and current_track['is_playing']:
                current_track_name = current_track['item']['name']
                current_track_artist = current_track['item']['artist']['name']
                current_track_album = current_track['item']['album']['name']

                current_track_artist_id = current_track['item']['artist']['id']
                current_artist = self.sp.artist(current_track_artist_id)
                current_track_genre = current_artist.get('genre', []) #this can return multiple genre btw, its any genre the artist is associated with.

                return f"{current_track_name}${current_track_artist}${current_track_album}${current_track_genre}"
            
            return None
        except Exception as e:
            logging.error(f"Spotipy API Error: {e}")
            return None
        
        

