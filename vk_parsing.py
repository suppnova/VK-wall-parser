import csv
import time
import configparser as cp

import requests


config = cp.ConfigParser()

config.read('config.ini')

ACCESS_TOKEN = config['ACCESS']['ACCESS_TOKEN']
API_VERSION = config['API']['API_VERSION']
url = config['API']['url']
domain = "pikabu"
start_date = "2021-05-12"
unix_start_date = time.mktime(time.strptime(f"{start_date} 00:00:00", '%Y-%m-%d %H:%M:%S'))
offset = config['API']['offset']
count = config['API']['count']
all_posts = []
flag = True


while flag:
    response = requests.get(url,
                            params={
                                "access_token": ACCESS_TOKEN,
                                "v": API_VERSION,
                                "domain": domain,
                                "offset": offset,
                                "count": count
                            }
                            )
    data = response.json()["response"]["items"]

    last_date = data[-1]["date"]
    if last_date < unix_start_date:
        for post in data:
            if post["date"] < unix_start_date:
                flag = False
                break
            else:
                all_posts.append(post)
    else:
        all_posts.extend(data)
        offset += 100


def get_attachments(post):
    attachments_links = []
    if "attachments" not in post:
        return attachments_links
    for attr in post["attachments"]:
        if attr["type"] == "photo":
            attachments_links.append(attr["photo"]["sizes"][-1]["url"])
        elif (attr_type := attr["type"]) in ["link", "audio", "doc"]:
            attachments_links.append(attr[attr_type]["url"])
        elif attr["type"] == "video":
            video_owner_id = str(attr["video"]["owner_id"])[1:]
            video_id = attr["video"]["id"]
            attachments_links.append(f"https://vk.com/video-{video_owner_id}_{video_id}")
    return attachments_links


def parse_post(post):
    post_id = post["id"] if "id" in post else "no_id"
    try:
        text = post["text"]
    except:
        text = ""
    try:
        attachments = get_attachments(post)
    except:
        attachments = ""
    try:
        attachments_amount = len(post["attachments"])
    except:
        attachments_amount = 0
    try:
        likes = post["likes"]["count"]
    except:
        likes = 0
    try:
        reposts = post["reposts"]["count"]
    except:
        reposts = 0
    try:
        comments = post["comments"]["count"]
    except:
        comments = 0
    return post_id, text, attachments, attachments_amount, likes, reposts, comments


def write_file(posts):
    with open("lfd.csv", "w") as fi:
        pen = csv.writer(fi)
        pen.writerow(("id", "text", "attachments", "attachments_amount", "likes", "reposts", "comments"))
        for post in posts:
            pen.writerow(parse_post(post))
