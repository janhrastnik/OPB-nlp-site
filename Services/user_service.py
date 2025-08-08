from Data.repo import Repo
from Data.models import User
from argon2 import PasswordHasher

# this class contains calls that deal with the user
# that for example includes registration, login, cookies etc.

class UserService:
    def __init__(self):
        self.repo = Repo()

    def register_user(self, email: str, nickname: str, password: str):
        # TODO: make sure user's email or nickname doesn't already exist

        ph = PasswordHasher()

        hashed_password = ph.hash(password)
        
        self.repo.add_new_user(email, nickname, hashed_password)

    def get_all_users(self):
        self.repo.get_all_users()

    def user_exists(self, email: str) -> bool:
        return self.repo.user_exists(email)

    def login(self, email: str, password: str) -> User | bool:
        user = self.repo.get_user(email)
        ph = PasswordHasher()

        if ph.verify(user.password, password):
            # correct password

            return user

        return False
    
    # TODO: add methods that register and login the user
