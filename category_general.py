# get the list page data

import requests
import time
import pymongo
import json
import sys
from pymongo import MongoClient

country = sys.argv[1]
category_param = sys.argv[2]
loopcount = sys.argv[3]
print("country is " + country + "category is " + category_param)
category_url = "https://news-af.op-mobile.opera.com/" + country + "/en/v1/news/category/"
main_url = "https://news-af.op-mobile.opera.com/" + country + "/en/v1/news/main"
#your own user id
user = "XXXX"
startTime = int(time.time())
session = requests.Session()

client = MongoClient('localhost', 27017)
db = client['opera' + country]
collection = db[category_param]

requestedJson = {"news_id_list": {}, "version": "3"}


def refreshcategory(category):
    topnews = []
    normal = []
    multiimage = []

    headers_base = {
        "user-agent": "Opera News/4.3.2254.129657/52.0.2743.10 (Android 4.4.4)"
    }

    param = {
        "product": "news",
        "features": "130829",
        "ac": "wifi",
        "lang": "zh",
        "category_id": category,
        "uid": user,
        "exclude": "summary",
        "referrer": "preload",
        "action": "refresh"
    }

    contents = session.post(category_url + category, params=param, headers=headers_base)
    for info in contents.json()["articles"]:
        if "top_news" in info["type"]:
            jsonarr = info["articles"]
            for json in jsonarr:
                if json.get("social_info", {}) is None:
                    json["social_info"] = {}
                listinfo = {
                    "original_url": json["original_url"],
                    "source": json["source"],
                    "title": json["title"],
                    "is_transcoded": json["is_transcoded"],
                    "open_type": json["open_type"],
                    "type": info["type"],
                    "subtype": json["type"],
                    "category": json["category"],
                    "comment_num": json["comment_num"],
                    "reports": json["reports"],
                    "shared_count": json.get("social_info", {}).get("shared_count", -1),
                    "total_emotions": json.get("social_info", {}).get("total_emotions", -1),
                    "total_like_count": json.get("social_info", {}).get("total_like_count", -1),
                    "total_shared_count": json.get("social_info", {}).get("total_shared_count", -1)

                }
                topnews.append(json["news_entry_id"])
                result = collection.update_one({"original_url": json["original_url"]}, {'$set': listinfo}, upsert=True)
        elif info["title"] != "":
            if info.get("social_info", {}) is None:
                info["social_info"] = {}
            listinfo = {
                "original_url": info["original_url"],
                "source": info["source"],
                "title": info["title"],
                "is_transcoded": info["is_transcoded"],
                "open_type": info["open_type"],
                "subtype": info["type"],
                "category": info["category"],
                "comment_num": info["comment_num"],
                "reports": info["reports"],
                "shared_count": info.get("social_info", {}).get("shared_count", -1),
                "total_emotions": info.get("social_info", {}).get("total_emotions", -1),
                "total_like_count": info.get("social_info", {}).get("total_like_count", -1),
                "total_shared_count": info.get("social_info", {}).get("total_shared_count", -1)
            }
            if info["type"] == "normal":
                normal.append(info["news_entry_id"])
            elif info["type"] == "multi_image":
                multiimage.append(info["news_entry_id"])
            result = collection.update_one({"original_url": info["original_url"]}, {'$set': listinfo}, upsert=True)
    if len(topnews) != 0:
        requested = {
            "top_news": topnews,
            "multi_image": multiimage,
            "normal": normal
        }
    else:
        requested = {
            "multi_image": multiimage,
            "normal": normal
        }
    requestedJson["news_id_list"].update({contents.json()["request_id"]: requested})


def loadcategory(category, time):
    topnews = []
    normal = []
    multiimage = []
    headers_base = {
        "user-agent": "Opera News/4.3.2254.129657/52.0.2743.10 (Android 4.4.4)"
    }

    param = {
        "product": "news",
        "features": "130829",
        "ac": "wifi",
        "lang": "zh",
        "category_id": category,
        "uid": user,
        "exclude": "summary",
        "action": "load_more",
        "load_more_count": time
    }

    contents = session.post(category_url + category, params=param, data=json.dumps(requestedJson), headers=headers_base)
    for info in contents.json()["articles"]:
        if "top_news" in info["type"]:
            jsonarr = info["articles"]
            for jsonparam in jsonarr:
                if jsonparam.get("social_info", {}) is None:
                    jsonparam["social_info"] = {}
                listinfo = {
                    "original_url": jsonparam["original_url"],
                    "source": jsonparam["source"],
                    "title": jsonparam["title"],
                    "is_transcoded": jsonparam["is_transcoded"],
                    "open_type": jsonparam["open_type"],
                    "type": info["type"],
                    "subtype": jsonparam["type"],
                    "category": jsonparam["category"],
                    "comment_num": jsonparam["comment_num"],
                    "reports": jsonparam["reports"],
                    "shared_count": jsonparam.get("social_info", {}).get("shared_count", -1),
                    "total_emotions": jsonparam.get("social_info", {}).get("total_emotions", -1),
                    "total_like_count": jsonparam.get("social_info", {}).get("total_like_count", -1),
                    "total_shared_count": jsonparam.get("social_info", {}).get("total_shared_count", -1)
                }
                topnews.append(jsonparam["news_entry_id"])
                result = collection.update_one({"original_url": jsonparam["original_url"]}, {'$set': listinfo}, upsert=True)
        else:
            if info.get("social_info", {}) is None:
                info["social_info"] = {}
            listinfo = {
                "original_url": info["original_url"],
                "source": info["source"],
                "title": info["title"],
                "is_transcoded": info["is_transcoded"],
                "open_type": info["open_type"],
                "subtype": info["type"],
                "category": info["category"],
                "comment_num": info["comment_num"],
                "reports": info["reports"],
                "shared_count": info.get("social_info", {}).get("shared_count", -1),
                "total_emotions": info.get("social_info", {}).get("total_emotions", -1),
                "total_like_count": info.get("social_info", {}).get("total_like_count", -1),
                "total_shared_count": info.get("social_info", {}).get("total_shared_count", -1)
            }
            if info["type"] == "normal":
                normal.append(info["news_entry_id"])
            elif info["type"] == "multi_image":
                multiimage.append(info["news_entry_id"])
            result = collection.update_one({"original_url": info["original_url"]}, {'$set': listinfo}, upsert=True)
    print("\n" + "now is the " + str(time) + "time")
    if len(topnews) != 0:
        requested = {
            "top_news": topnews,
            "multi_image": multiimage,
            "normal": normal
        }
    else:
        requested = {
            "multi_image": multiimage,
            "normal": normal
        }
    requestedJson["news_id_list"].update({contents.json()["request_id"]: requested})


refreshcategory(category=category_param)
for i in range(int(loopcount)):
    loadcategory(category=category_param, time=i)
