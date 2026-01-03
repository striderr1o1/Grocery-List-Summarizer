from applogic.mongoDB_conn import MongoDBConnector
from applogic.auth import authentication
mdb = MongoDBConnector()
def testfunc():
    authobj = authentication(mdb)
    print(authobj.authenticate_user("mustafa123", "anger123"))


