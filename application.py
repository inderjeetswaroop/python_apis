from flask import Flask, jsonify, render_template, request
import bson.json_util as json_util
from bson.objectid import ObjectId
from flask_cors import CORS
# Temporary imports
from pytz import timezone 
import datetime
# Temporary imports
import databaseconnection
import addUserbysadmin
import userregister
import userlogin
import uploadaudio
import os 



client = databaseconnection.connectDb()
db = client["pinak"]

application = Flask(__name__)
application.secret_key  = b'inderjeet!@#$%4322'
CORS(application)
 
@application.route("/")
def hello_world():
    pinakuser = db.users
    usercollection = pinakuser.find()
    # ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S')
    d = datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime('%d-%m-%Y')
    return json_util.dumps(usercollection)

@application.route("/upload-user-audio", methods=['POST'])
def uploadAudios():
    response = uploadaudio.uploadmyaudio(request)
    return response
    
@application.route("/uploaded-user-audio-list/<userId>/<merchantId>")
def uploadedAudiosList(userId,merchantId):
    response = uploadaudio.getAllAudios(userId,merchantId)
    return response

@application.route("/user-register", methods=['POST'])
def add():
    response = userregister.add_new_user(request)
    return response

@application.route("/user-login-data", methods=['POST'])
def user_login():
    response = userlogin.login_data(request)
    return response

@application.route("/single-audio-info",methods=['POST'])
def singleAudioInfo():
    response = uploadaudio.getAudiosInfo(request)
    return response    


@application.route("/audio-list-by-date",methods=['POST'])
def AudioInfoDateWise():
    response = uploadaudio.getAudioBydate(request)
    return response    


@application.route("/get-single-user-detail/<userid>/<merchantId>")            
@application.route("/get-single-user-detail/<userid>")
def get_single_user_detail(userid,merchantId=0):
    pinakuser = db.users
    if merchantId == 0:
        fUser = pinakuser.find_one( { "_id" : ObjectId(userid) })
    else:
        fUser = pinakuser.find_one({"merchant_id" : merchantId },{"user_phone":1,"_id":0})
        userphone = fUser['user_phone']
        userdbName = 'userdb_'+str(userphone)+'_'+str(merchantId)
        userdb = client[userdbName]
        userCol = userdb[userid]
        fUser = userCol.find_one()
        
    return json_util.dumps(fUser)

@application.route("/get-employee-user-list/<userid>/<merchatId>")
def get_manager_user_list(userid,merchatId):
    pinakuser = db.users
    adminDbDetail = pinakuser.find_one({"merchant_id":merchatId},{"user_phone":1,"_id":0})
    adminPhone = adminDbDetail["user_phone"]
    userdbName = 'userdb_'+str(adminPhone)+'_'+str(merchatId)
    userdb = client[userdbName]
    userCollections = userdb[userid]
    user_list = userCollections.find({"user_name":{"$exists":True},"manager":{ "$ne": "0" }})
    return json_util.dumps(user_list)            

@application.route("/get-admins-user-list/<userid>")
def get_user_details(userid,merchatId=0):
    pinakuser = db.users
    fUser = pinakuser.find_one( { "_id" : ObjectId(userid) })
    userdbName = 'userdb_'+str(fUser['user_phone'])+'_'+str(fUser['merchant_id'])
    
    userdb = client[userdbName]
    admin_user_col = "admin_"+str(fUser['user_phone'])
    userCollections = userdb[admin_user_col]
    user_list = userCollections.find({"user_name":{"$exists":True}})
    return json_util.dumps(user_list)            
    

@application.route("/add-new-user-level", methods=['POST'])
def add_admin_user():
    response = addUserbysadmin.add_user_by_admin(request)
    return response

@application.route("/add-new-employee-level/<merchantId>", methods=['POST'])
def add_manager_user(merchantId):
    response = addUserbysadmin.add_user_by_manager(request,merchantId)
    return response



""" if __name__ == "__main__":
   application.run(debug=True) """
    
