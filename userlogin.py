import bson.json_util as json_util
import databaseconnection
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256


client = databaseconnection.connectDb()
db = client["pinak"]

def login_data(request):
    pinakuser = db.users

    useremail = request.form.get("useremail")
    upassword = request.form.get('userpass')
    usertype = request.form.get('usertype')
    merchant = request.form.get('merch_id')
    
    if usertype == "0":
        check = pinakuser.count_documents( { "$or" : [{ "user_email": useremail }, { "user_phone":useremail } ] })
        if check > 0:
            fUser = pinakuser.find_one( { "$or" : [{ "user_email": useremail }, { "user_phone":useremail } ]})
            checkpass = pbkdf2_sha256.verify(upassword, fUser["user_pass"])
            userid = fUser["_id"]
            if checkpass == True:
                return json_util.dumps({
                    "status": "success",
                    "message": f'{userid}',
                    "iAMUser":"admin",
                    "merchant": f'{fUser["merchant_id"]}'
                    })
            else:
                return json_util.dumps({
                    "status": "failed",
                    "message": "0"
                    })
        else:
            return json_util.dumps({
                    "status": "failed",
                    "message": "0"
                    })
    else:
        check = pinakuser.count_documents({ "merchant_id": merchant } )
        if(check > 0):
            adminDbDetail = pinakuser.find_one({ "merchant_id": merchant },{"user_phone":1,"_id":0})
            userdbName = "userdb_"+str(adminDbDetail["user_phone"])+"_"+str(merchant)
            userdb = client[userdbName]
            allCol = userdb.list_collection_names()
            if usertype == "1":
                utype = "manager"
                loginUser = "manager_"+useremail+"_"+merchant
            else:
                utype = "employee"
                loginUser = "employee_"+useremail+"_"+merchant

            iAmuserCollection = userdb[loginUser]
            iAMUser = iAmuserCollection.find_one({"user_name": useremail,"user_pass":upassword })
            
            if iAMUser is not None:
                return json_util.dumps({
                    "status": "success",
                    "message": f'{loginUser}',
                    "iAMUser":utype,
                    "merchant":merchant
                    })
            else:
                return json_util.dumps({
                    "status": "failed",
                    "message": "0"
                    })
                
                
        else:
            return json_util.dumps({
                    "status": "failed",
                    "message": "Wrong Merchant Id! Please Re-enter "
                    })