from flask import Flask, jsonify, render_template, request
import bson.json_util as json_util
import pymongo
import databaseconnection

application = Flask(__name__)

client = databaseconnection.connectDb()


@application.route("/")
def hello_world():
    userdb = client["pinak"]
    adminCol = userdb["users"]
    allenteries = adminCol.find()
    return json_util.dumps(allenteries)
    return "Hello there! I have some changes"

@application.route("/hello-world2")
def hello_world2():
    return "Hello world 2 there! I have been created by now"