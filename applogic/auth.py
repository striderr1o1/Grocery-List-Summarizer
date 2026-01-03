class authentication:
    auth_database_connector = None
    authenticated = False
    def __init__(self, auth_database):
        self.auth_database_connector = auth_database
        self._connectauthdb()

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
        if(password == json["password"] and username == json["username"]):
            return True
        return False