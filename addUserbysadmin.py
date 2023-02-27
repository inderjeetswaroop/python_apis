import bson.json_util as json_util
import databaseconnection
from bson.objectid import ObjectId


client = databaseconnection.connectDb()
db = client["pinak"]

def add_user_by_admin(request):
    pinakuser = db.users

    username = request.form.get("uname")
    user_fullname = request.form.get("fullName")
    userpass = request.form.get("upassword")
    usertype = request.form.get("usertype")
    userid = request.form.get('adminuser')
    manager_username = request.form.get('manager_username')
    if usertype == 1:
        prefix = "manager"
    else:    
        prefix = "employee"
    
    # start: Creating new collection for new user
    fUser = pinakuser.find_one( { "_id" : ObjectId(userid) })
    userphone = fUser['user_phone']
    mechant = fUser['merchant_id']
    userdbName = 'userdb_'+str(userphone)+'_'+str(mechant)
    userdb = client[userdbName]
    adminColName = "admin_"+userphone
    adminCol = userdb[adminColName]
    
    # Start : adding user to admin collection
    newUserDetails={
            "user_name": username,
            "user_fullname":user_fullname,
            "user_pass" : userpass,
            "user_type" : usertype,
            "user_status": 1,
            "merchant_id": mechant,
            "manager": manager_username,
            "admin_id": userid
        }
    # return json_util.dumps(usertype)
    if (usertype == "1"):
        checkExisted = adminCol.count_documents({"user_name":username})

        if checkExisted > 0:
            rstatus= "falied"
            rmessage= "User already existed! Please enter unique username."
            
        else:
            adminCol.insert_one(newUserDetails)
        # End : adding user to admin collection
            newUserCol = "manager_"+username+"_"+mechant
            userCollection = userdb[newUserCol]
            userCollection.insert_one(newUserDetails)
            
            rstatus = "success"
            rmessage = ""

    else:
        rstatus = "failed"
        rmessage = "Nothing"
        managerColName = "manager_"+manager_username+"_"+mechant
        managerCol = userdb[managerColName]
        managerCol.insert_one(newUserDetails)
        
        employColName = "employee_"+username+"_"+mechant
        userCollection = userdb[employColName]
        userCollection.insert_one(newUserDetails)
            
        rstatus = "success"
        rmessage = ""
    
    
    # end: Creating new collection for new user
    alluserCollections = adminCol.find({"user_name":{"$exists":True}})
    # lastid =pinakuser.insert_one(usr).inserted_id
    return json_util.dumps({
        "status": rstatus,
        "message": rmessage,
        "allusers": alluserCollections
    })

def add_user_by_manager(request,mechant):
    pinakuser = db.users

    username = request.form.get("uname")
    user_fullname = request.form.get("fullName")
    userpass = request.form.get("upassword")
    usertype = request.form.get("usertype")
    userid = request.form.get('adminuser')
    manager_username = request.form.get('manager_username')
    if usertype == 1:
        prefix = "manager"
    else:    
        prefix = "employee"
    
    
    fUser = pinakuser.find_one({"merchant_id" : mechant },{"user_phone":1,"_id":0})
    

    userphone = fUser['user_phone']
    userdbName = 'userdb_'+str(userphone)+'_'+str(mechant)
    userdb = client[userdbName]
    adminColName = userid
    adminCol = userdb[adminColName]
    
    # Start : adding user to admin collection
    newUserDetails={
            "user_name": username,
            "user_fullname":user_fullname,
            "user_pass" : userpass,
            "user_type" : usertype,
            "user_status": 1,
            "merchant_id": mechant,
            "manager": manager_username,
            "admin_id": userid
        }
    # return json_util.dumps(usertype)
    
    checkExisted = adminCol.count_documents({"user_name":username})

    if checkExisted > 0:
        rstatus= "falied"
        rmessage= "User already existed! Please enter unique username."
        
    else:
        adminCol.insert_one(newUserDetails)
    # End : adding user to admin collection
        newUserCol = "employee_"+username+"_"+mechant
        userCollection = userdb[newUserCol]
        userCollection.insert_one(newUserDetails)
        
        rstatus = "success"
        rmessage = ""

    
    
    
    # end: Creating new collection for new user
    alluserCollections = adminCol.find({"user_name":{"$exists":True},"manager":{ "$ne": "0" }})
    # lastid =pinakuser.insert_one(usr).inserted_id
    return json_util.dumps({
        "status": rstatus,
        "message": rmessage,
        "allusers": alluserCollections
    })

