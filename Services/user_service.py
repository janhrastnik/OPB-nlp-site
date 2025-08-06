from Data.repo import Repo
from argon2 import PasswordHasher

# this class contains calls that deal with the user
# that for example includes registration, login, cookies etc.

class UserService:
    def __init__(self):
        self.repo = Repo()

    def register_user(self, email, nickname, password):
        # TODO: make sure user's email or nickname doesn't already exist

        ph = PasswordHasher()

        hashed_password = ph.hash(password)
        
        self.repo.add_new_user(email, nickname, hashed_password)

    def get_all_users(self):
        self.repo.get_all_users()
    
    # TODO: add methods that register and login the user
