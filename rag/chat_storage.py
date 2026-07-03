import json
import os

CHAT_FILE = "chats/chat_sessions.json"

os.makedirs(
    "chats",
    exist_ok=True
)


def load_chats():

    if not os.path.exists(
        CHAT_FILE
    ):
        return {}

    try:

        with open(
            CHAT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


def save_chats(chats):

    with open(
        CHAT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chats,
            f,
            indent=4,
            ensure_ascii=False
        )