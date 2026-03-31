from fastapi import FastAPI
from auth_service import AuthService
from database import DatabaseManager
from music_service import MusicService

#testing spotify music tracking
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                               scope="user-read-currently-playing"))



db_tool = DatabaseManager("fitness_tracker.db")
auth_tool = AuthService()
music_tool = MusicService(sp)

class connection_service:
    def __init__(self, username, password, db, auth, music):
        self.username = username
        self.password = password
        self.db = db
        self.auth = auth
        self.music = music

    def signup(self): #if add_user fails, don't assign_user_id, if username exists, go to signin function
        unique_user_id = AuthService.create_new_user_id()
        
        assign_user_id = self.db.assign_user_id(self.username, unique_user_id)
        if assign_user_id == False:
            print("Username taken")
            test_connection.signin()
            return
        
        password_data = self.auth.hash_password(self.password)
        self.db.add_user(unique_user_id, password_data)
        print("user signed up")

    def signin(self):
        user_id = self.db.get_user_id(self.username)
        password_data = self.db.get_password_data(user_id)

        verify_password = self.auth.verify_password(password_data, self.password)
        if verify_password: 
            print("Succesful Sign-in") #testing
        else:
            print("Sign-in failed") #testing

    def get_music_test(self):
        current_track_test = self.music.get_music_data()
        print(current_track_test)



test_username = input("Username: ")
test_password = input("Password: ")

test_connection = connection_service(test_username, test_password, db_tool, auth_tool, music_tool)

#test_connection.signup()
test_connection.get_music_test()

#need to make ti so every user has to connect their spotify, rn when one connected, others just use that spotify account data.