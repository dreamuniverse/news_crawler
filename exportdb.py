# 导出为csv文件
import codecs
import csv
import pymongo
import sys

country = sys.argv[1]
category_param = sys.argv[2]
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['opera' + country]
collection = db[category_param]
# 查询库中数据
cursor = collection.find()
with codecs.open('data_' + category_param + "_" + country + '.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 先写入columns_name
    writer.writerow(["original_url", "category", "comment_num", "is_transcoded", "open_type", "reports", "shared_count",
                     "source", "subtype", "title", "total_emotions", "total_like_count", "total_shared_count"])
    # 写入多行用writerows
    for data in cursor:
        writer.writerows([[data["original_url"], data["category"], data["comment_num"], data["is_transcoded"],
                           data["open_type"], data["reports"], data["shared_count"], data["source"], data["subtype"],
                           data["title"], data["total_emotions"], data["total_like_count"],
                           data["total_shared_count"]]])
