import json
import os

FILE = "chats/settings.json"


def save_last_chat(chat_id):

    with open(FILE, "w") as f:

        json.dump(
            {
                "last_chat": chat_id
            },
            f
        )


def load_last_chat():

    if not os.path.exists(FILE):

        return None

    with open(FILE) as f:

        return json.load(f).get(
            "last_chat"
        )