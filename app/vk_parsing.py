import time

import requests

from app.models.post import Post
from app.utils.config import ACCESS_TOKEN, API_VERSION, COUNT, OFFSET, URL
from app.utils.times import get_unix_time

all_posts = []


def get_all_posts():
    return all_posts


def process_link(url):
    link = url.split("/")[-1]

    if link.startswith("id") and (user_id := link[2:]).isdigit():
        return "owner_id", user_id
    if link.startswith("public") and (public_id := link[6:]).isdigit():
        return "owner_id", f"-{public_id}"
    return "domain", link


def fetch_posts_after_start_date(url, date):
    global all_posts
    all_posts = []
    local_offset = OFFSET
    link_key, link_value = process_link(url)
    flag = True
    datetime_until = get_unix_time(date)
    while flag:
        time.sleep(0.5)
        response = requests.get(
            URL,
            params={
                "access_token": ACCESS_TOKEN,
                "v": API_VERSION,
                link_key: link_value,
                "offset": local_offset,
                "count": COUNT,
            },
        )
        data = response.json()["response"]["items"]

        if not data:
            print("data is empty")
            break

        if data[-1]["date"] < datetime_until:

            for post in data:
                if "is_pinned" not in post and post["date"] < datetime_until:
                    flag = False
                    break
                else:
                    all_posts.append(Post(post))
        else:
            all_posts.extend([Post(post) for post in data])
            local_offset += 100


# def write_file(posts):
#     with open("../lfd.csv", "w", encoding="utf-8") as fi:
#         pen = csv.writer(fi)
#         pen.writerow(
#             (
#                 "id",
#                 "text",
#                 "attachments",
#                 "attachments_amount",
#                 "likes",
#                 "reposts",
#                 "comments",
#             )
#         )
#         for post in posts:
#             pen.writerow(
#                 (
#                     post.id,
#                     post.text,
#                     post.attachments,
#                     post.attachments_amount,
#                     post.likes,
#                     post.reposts,
#                     post.comments,
#                 )
#             )
