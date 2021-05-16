class Post:
    def __init__(self, post):
        self.id = post["id"] if "id" in post else "no_id"
        self.text = post["text"] if "text" in post else ""
        self.date = post["date"] if "date" in post else 0
        self.attachments = self.extract_attachments(post)
        self.attachments_amount = (
            len(post["attachments"]) if "attachments" in post else 0
        )
        self.likes = post["likes"]["count"] if "likes" in post else 0
        self.reposts = post["reposts"]["count"] if "reposts" in post else 0
        self.comments = post["comments"]["count"] if "comments" in post else 0

    @classmethod
    def extract_attachments(cls, post):
        attachments_links = []
        if "attachments" not in post:
            return attachments_links
        for att in post["attachments"]:
            if att["type"] == "photo":
                attachments_links.append(att["photo"]["sizes"][-1]["url"])
            elif (attr_type := att["type"]) in ["link", "audio", "doc"]:
                attachments_links.append(att[attr_type]["url"])
            elif att["type"] == "video":
                video_owner_id = str(att["video"]["owner_id"])[1:]
                video_id = att["video"]["id"]
                attachments_links.append(
                    f"https://vk.com/video-{video_owner_id}_{video_id}"
                )
        return attachments_links

    def get_attachments_row(self):
        row = ""

        for attachment in self.attachments:
            row += f"'{attachment}',"

        return row[:-1]

    def transform_to_csv(self):
        return (
            str(self.id),
            f'"{self.text}"',
            f'"[{self.get_attachments_row()}]"',
            str(self.attachments_amount),
            str(self.likes),
            str(self.reposts),
            str(self.comments),
        )
