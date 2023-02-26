from flask import Flask, jsonify, render_template, request
import bson.json_util as json_util
# import databaseconnection
import testingImport
# import pymongo
import ssl

application = Flask(__name__)

# client = pymongo.MongoClient("mongodb+srv://mongoadmin:tHca1yxBGYrplCtj@pai-mongo-cluster.rwmz5rj.mongodb.net/?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs=ssl.CERT_NONE)


@application.route("/")
def hello_world():
    """ userdb = client["pinak"]
    adminCol = userdb["users"]
    allenteries = adminCol.find()
    return json_util.dumps(allenteries) """
    return "Hello there! I have some changes"

@application.route("/hello-world2")
def hello_world2():
    return testingImport.thisistesting()

