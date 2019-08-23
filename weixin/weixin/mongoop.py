from pymongo import MongoClient
from settings import *
def getCollection(collectionName):
    client=MongoClient(host=mongo_host,port=mongo_port)
    db=client[mongo_db_name]
    collection=db[collectionName]
    return collection

def getCollectionCount(collectionName):
    coll=getCollection(collectionName)
    count=coll.find().count()
    return count

def pageQuery(collectionName,queryFilter=None,pageSize=1,pageNo=1):
    skip=pageSize*(pageNo-1)
    coll=getCollection(collectionName)
    pageRecord=coll.find(queryFilter).limit(pageSize).skip(skip)
    return pageRecord
