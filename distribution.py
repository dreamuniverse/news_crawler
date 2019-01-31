# 导出为新的数据库，统计对应数据
import pymongo
import sys

country = sys.argv[1]
category_param = sys.argv[2]
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['opera' + country]
collection = db[category_param]
# 查询库中数据
cursor = collection.find()

client_new = pymongo.MongoClient('127.0.0.1', 27017)
db_new = client_new['distribution_' + country]
collection_new = db_new[category_param]

for data in cursor:
    data["count"] = 1
    cursor_new = collection_new.find({"source": data["source"]})
    if cursor_new.count() > 0:
        data_new = cursor_new[0]
    else:
        data_new = {}
    listinfo = {
        "shared_count": data["total_shared_count"] + data_new.get("total_shared_count", 0),
        "count": data["count"] + data_new.get("count", 0),
        "like_count": data["total_like_count"] + data_new.get("total_like_count", 0),
        "comment_num": data["comment_num"] + data_new.get("comment_num", 0)
    }
    collection_new.update_one({"source": data["source"]}, {'$set': listinfo}, upsert=True)
