from passlib.context import CryptContext
from pymongo.errors import PyMongoError, ConnectionFailure

class authentication:
    auth_database_connector = None
    authenticated = False
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def __init__(self, auth_database_conn):
        self.auth_database_connector = auth_database_conn
        #self._connectauthdb()

    def _connectauthdb(self):
        try:
            self.auth_database_connector.connectToAuthDatabase()
            self.authenticated = True
        except ConnectionFailure as e:
            print("auth db not connected: ", {e})
            raise

    def authenticate_user(self, username, password):
        #check if user exists, if yes, match password
        user_data = self.auth_database_connector.get_user(username)
        
        try:
            json = user_data[0]
        except IndexError:
            return False

        if(self._verify_password(password, json["password"]) and username == json["username"]):
            return True
        return False

    def create_user(self, username, password):
        # hash password
        hashed_password = self._hash_the_password(password)
        self.auth_database_connector.InsertUser(username, hashed_password)
                   

    def check_user_exists(self, username):
        database = self.auth_database_connector.client2["authentication"]
        collection = database["username_passwords"]
        resp = collection.find_one({"username": username})
        if resp: # adding comment in vim
            return True
        return False

    def _hash_the_password(self, password):
        return self.pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
