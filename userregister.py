import bson.json_util as json_util
import databaseconnection
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
from random import randint


client = databaseconnection.connectDb()
db = client["pinak"]

def add_new_user(request):
    pinakuser = db.users

    useremail = request.form.get('useremail')
    userphone = request.form.get('userphone')
    if request.method == "POST":
        
        check = pinakuser.count_documents( { "$or" : [{ "user_email": useremail }, { "user_phone":userphone } ] })
        if check > 0 :
            return json_util.dumps({
            "status": "failed",
            "message": "Either Email or Phone already registered!"
            })
        else:
            merchantId = str(randint(1000000000, 9999999999))
            
            usr ={
                "merchant_id":merchantId,
                "user_email": useremail,
                "email_verified": 0,
                "user_status": 1,
                "user_name": request.form.get('username'),
                "user_pass": pbkdf2_sha256.hash(request.form.get('userpass')),
                "user_phone": userphone,
                "user_company": request.form.get('usercompany'),
                "created_at": datetime.datetime.now()
            }
            pinakuser.insert_one(usr)
            userdb = client["userdb_"+userphone+"_"+merchantId]
            userCollection = userdb["admin_"+userphone]
            initData = {
                    'init':"0",
                    "user":userphone
            }
            userCollection.insert_one(initData)
            # lastid =pinakuser.insert_one(usr).inserted_id
            return json_util.dumps({
            "status": "success",
            "message": "You have been registered successfully!"
            })

    else:
        return json_util.dumps({
            "status": "failed",
            "message": ""
        })