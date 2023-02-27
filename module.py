import bson.json_util as json_util
import databaseconnection

client = databaseconnection.connectDb()
db = client["pinak"]

def get_all_users():
    pinakuser = db.users
    allusers = pinakuser.find()
    return json_util.dumps(allusers)

""" class GFG:
      
    # methods
    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b """
  
""" # explicit function      
def method():
    print("GFG") """