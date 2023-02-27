import bson.json_util as json_util
from werkzeug.utils import secure_filename
import boto3
import uuid
import databaseconnection
import datetime
import os 
import getMerchantInfo
from bson.objectid import ObjectId

os.listdir()

client = databaseconnection.connectDb()
db = client["pinak"]

# boto3 
uploadclient = boto3.client("s3",
    aws_access_key_id="AKIATC44XYSY4QG4NUWP",
    aws_secret_access_key="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",
)
# boto3 

s3_url = "https://pinak-audios.s3.ap-south-1.amazonaws.com/"


def uploadmyaudio(request):
    
    if request.method == 'POST':
        
        userId = request.form.get('userId')
        merchantId = request.form.get('merchant')
        img = request.files["audiofile"]

        userCollection  = request.form.get("user_collection")


        filename = secure_filename(img.filename)
        img.save(filename) # This line will save the file locally
        # img.save(os.path.join(app.instance_path, 'htmlfi', secure_filename(img.filename)))
        new_file_name =  uuid.uuid4().hex + filename
        response = uploadclient.upload_file(
            Bucket = "pinak-audios",
            Filename = filename,
            Key = new_file_name
        )

        # adding audio details to database
        pinakuser = db.users
        fUser = pinakuser.find_one({"merchant_id" : merchantId },{"user_phone":1,"_id":0})
        
        userphone = fUser['user_phone']
        userdbName = 'userdb_'+str(userphone)+'_'+str(merchantId)
        
        userdb = client[userdbName]
        adminCol = userdb[userId]
        # allenteries = adminCol.find()
        
        file_url = s3_url + new_file_name

        newAudioDetails = {
            "file_type":"audio",
            "file_keyName": new_file_name,
            "file_url":file_url,
            "upload_time":datetime.datetime.now(),

        }
        adminCol.insert_one(newAudioDetails)
        
        allenteries = adminCol.find({"file_type":"audio"})
        
        status = "success"
        msg = "Audio is uploaded successfully"

        
    else:
        status = "failed"
        msg = "Audio is not uploaded! Please try again"
        allenteries={}
    

    return json_util.dumps({
        "status": status,
        "message": msg,
        "allenteries":allenteries
        })

def getAllAudios(userId,merchantId):
    
    pinakuser = db.users
    fUser = pinakuser.find_one({"merchant_id" : merchantId },{"user_phone":1,"_id":0})
    
    userphone = fUser['user_phone']
    userdbName = 'userdb_'+str(userphone)+'_'+str(merchantId)
    
    userdb = client[userdbName]
    adminCol = userdb[userId]
    allenteries = adminCol.find({"file_type":"audio"})
    return json_util.dumps(allenteries)

def getAudiosInfo(request):
    merchantId = request.form.get('merch_id')
    usercol = request.form.get('username')
    audioId = request.form.get('audioId')
    usertype = request.form.get('userType')
    
    userdb = getMerchantInfo.info(merchantId)
    usercollection = userdb[usercol]
    audioInfo = usercollection.find_one( { "_id" : ObjectId(audioId) })

    return json_util.dumps(audioInfo)

def getAudioBydate(request):
    merchantId = request.form.get('merch_id')
    usercol = request.form.get('username')
    audiodate = request.form.get('audioDate')
    usertype = request.form.get('userType')
    formatedDate = datetime.datetime.strptime(audiodate, "%Y-%m-%d").strftime('%d-%m-%Y')
    userdb = getMerchantInfo.info(merchantId)
    usercollection = userdb[usercol]
    result = usercollection.find({'date_time': {'$regex':formatedDate} })
    
    return json_util.dumps(result)
