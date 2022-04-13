

POSTS_MAPPING = {
    "account_id": {"type": "integer"},

    "chat_id": {"type": "long"},
    "message_id": {"type": "long"},
    "text": {"type": "text"},
    "published": {"type": "date"},

    ":views": {"type": "integer"},
    ":forwards": {"type": "integer"},
    ":replies": {"type": "integer"},

    ':photos': {"type": "text"},
    ':videos': {"type": "text"},
}


PROCESSES_MAPPING = {
    "account_id": {"type": "integer"},
    "user_id": {"type": "long"},
    "channel_id": {"type": "long"},
    "task_id": {"type": "text"},

    "updated": {"type": "date"},
    "status": {"type": "keyword"},
}
