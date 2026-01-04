# from passlib.context import CryptContext
from pymongo.errors import PyMongoError, ConnectionFailure
class authentication:
    auth_database_connector = None
    authenticated = False
    def __init__(self, auth_database):
        self.auth_database_connector = auth_database
        # self._connectauthdb()

    def _connectauthdb(self):
        try:
            self.auth_database_connector.connectToAuthDatabase()
            self.authenticated = True
        except ConnectionFailure as e:
            print("auth db not connected: ", {e})
            raise

    def authenticate_user(self, username, password):
        #check if user exists, if yes, match password
        json = self.auth_database_connector.get_user(username)
        json = json[0]

        if(self._verify_password(password, json["password"]) and username == json["username"]):
            return True
        return False

    def create_user(self, username, password):
        # hash password
        hashed_password = self._hash_the_password(password)
        self.auth_database_connector.insertUser(username, hashed_password)


    def check_user_exists(self, username):
        database = self.auth_database_connector
        collection = database["username_passwords"]
        resp = collection.find_one({"username": username})
        if resp == True:
            return True
        return False

    def _hash_the_password(self, password):
        # pwd_context = CryptContext(
        #     schemes=["bcrypt"],
        #     deprecated="auto"
        # )
        # return pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        # pwd_context = CryptContext(
        #     schemes=["bcrypt"],
        #     deprecated="auto"
        # )
        # return pwd_context.verify(password, hashed_password)
