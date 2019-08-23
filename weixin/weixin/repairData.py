import pymongo
import random
from settings import *
from mongoop import *
client =pymongo.MongoClient(host=mongo_host,port=mongo_port)
db = client[mongo_db_name]
collection = db[mongo_db_collection]

def repairData():
    results=collection.find()
    for result in results:
        _id=result['_id']
        condition={'_id':_id}
        desc=getPicDesc()
        result['pic_desc']=desc
        info=collection.update_one(condition,{'$set':result})
        print(info)


def getPicDesc():
    desc = getWord("interjection") + " " + getWord("subject") + " " + getWord(
        "object") + " " + getWord("action") + " " + getWord("location") + " " + getWord(
        "time") + " in " + getWord("country")
    # 感叹词+主语+宾语+行为+地点+时间+国家
    desc=getWord("interjection")+" "+getWord("subject")+" "+getWord("object")+" "+getWord("action")+" "+getWord("location")+" "+getWord("time")+" in "+getWord("country")
    print(desc)
    return desc

def getWord(collectionName):
    subjectCount = getCollectionCount(collectionName)
    subjectIndex = random.randint(1, subjectCount)
    print(subjectIndex)
    results = pageQuery(collectionName, None, 1, subjectIndex)
    result = results[0]
    word = result['ename']
    return word


if __name__=="__main__":
    print("main function.")
    repairData()