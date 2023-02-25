from flask import Flask
import testingImport
application = Flask(__name__)

@application.route("/")
def hello_world():
    return "Hello there"
    
@application.route("/hello-world2")
def hello_world2():
    return testingImport.thisistesting()    