import pymongo

def connectDb():
    return pymongo.MongoClient("mongodb+srv://mongoadmin:tHca1yxBGYrplCtj@pai-mongo-cluster.rwmz5rj.mongodb.net/?retryWrites=true&w=majority")