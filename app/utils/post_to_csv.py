headers = (
    "id",
    "text",
    "attachments",
    "attachments_amount",
    "likes",
    "reposts",
    "comments",
)


def create_csv(data):
    csv_data = ",".join(headers) + "\n"
    for post in data:
        csv_data += ",".join(post.transform_to_csv()) + "\n"

    return csv_data
