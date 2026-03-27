from fastapi import FastAPI
from auth_service import AuthService
from database import DatabaseManager

db_tool = DatabaseManager("fitness_tracker.db")
auth_tool = AuthService()

class connection_service:
    def __init__(self, username, password, db, auth):
        self.username = username
        self.password = password
        self.db = db
        self.auth = auth

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



test_username = input("Username: ")
test_password = input("Password: ")

test_connection = connection_service(test_username, test_password, db_tool, auth_tool)

# 2. Call the method on that specific instance
test_connection.signup()