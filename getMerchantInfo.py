import bson.json_util as json_util
import databaseconnection

client = databaseconnection.connectDb()
db = client["pinak"]

def info(merchantId):
    pinakuser = db.users
    fUser = pinakuser.find_one({"merchant_id" : merchantId },{"user_phone":1,"_id":0})
    
    userphone = fUser['user_phone']
    userdbName = 'userdb_'+str(userphone)+'_'+str(merchantId)
    userdb = client[userdbName]
    return userdb