from app.models.post import Post


def test_post_pos():
    post = Post(
        {
            "id": 54,
            "text": "Post text",
            "date": 1620827160,
            "attachments": [
                {
                    "type": "photo",
                    "photo": {"sizes": [{"url": ""}, {"url": "photo_link"}]},
                },
                {"type": "link", "link": {"url": "link"}},
                {"type": "audio", "audio": {"url": "audio/25"}},
                {"type": "doc", "doc": {"url": "docs/m"}},
                {"type": "video", "video": {"owner_id": "-27", "id": "video"}},
            ],
            "reposts": {"count": 1},
            "likes": {"count": 2},
            "comments": {"count": 3},
        }
    )
    assert post.id == 54
    assert post.text == "Post text"
    assert post.date == 1620827160
    assert post.attachments == [
        "photo_link",
        "link",
        "audio/25",
        "docs/m",
        "https://vk.com/video-27_video",
    ]
    assert post.reposts == 1
    assert post.likes == 2
    assert post.comments == 3


def test_post_no_data():
    post = Post({"post_type": "no_data_post"})

    assert post.id == "no_id"
    assert post.text == ""
    assert post.date == 0
    assert post.attachments == []
    assert post.reposts == 0
    assert post.likes == 0
    assert post.comments == 0
