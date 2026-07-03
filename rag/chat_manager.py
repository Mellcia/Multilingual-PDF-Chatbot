import uuid
import os
import shutil
from rag.chat_storage import (
    load_chats,
    save_chats
)
from rag.vector_store import (
    delete_chat_collection
)
from datetime import datetime


def create_chat(username):
    chats = load_chats()

    chat_id = str(
        uuid.uuid4()
    )

    # Scoping the dictionary entry to include a 'username' key for filtering
    chats[chat_id] = {
        "username": username.strip().lower(),
        "title": "New Chat",
        "messages": [],
        "files": [],
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now())
    }

    save_chats(chats)
    return chat_id


def get_chat(chat_id):
    chats = load_chats()
    return chats.get(
        chat_id,
        None
    )


def update_chat_messages(
        chat_id,
        messages
):
    chats = load_chats()

    if chat_id in chats:
        chats[chat_id][
            "messages"
        ] = messages
        chats[chat_id]["updated_at"] = str(
            datetime.now()
        )
        save_chats(chats)


def rename_chat(
        chat_id,
        new_title
):
    chats = load_chats()

    if chat_id in chats:
        chats[chat_id][
            "title"
        ] = new_title

        chats[chat_id][
            "updated_at"
        ] = str(datetime.now())

        save_chats(chats)


def delete_chat(
        chat_id,
        username
):
    chats = load_chats()

    if chat_id in chats:
        delete_chat_collection(
            chat_id
        )
        
        # Clean up the isolated user-specific workspace folders on session deletion
        chat_workspace_dir = os.path.join("workspace_data", username.strip().lower(), chat_id)
        if os.path.exists(chat_workspace_dir):
            try:
                shutil.rmtree(chat_workspace_dir)
            except Exception:
                pass

        del chats[chat_id]
        save_chats(chats)


def get_all_chats(username):
    """Loads all chats but filters them to return only those belonging to the given username."""
    all_chats = load_chats()
    target_user = username.strip().lower()
    
    user_chats = {
        cid: cinfo for cid, cinfo in all_chats.items()
        if cinfo.get("username", "").strip().lower() == target_user
    }
    return user_chats


def add_file_to_chat(
        chat_id,
        file_name
):
    chats = load_chats()

    if chat_id in chats:
        if file_name not in chats[
            chat_id
        ]["files"]:

            chats[chat_id][
                "files"
            ].append(file_name)

            save_chats(chats)


def get_chat_files(
        chat_id
):
    chats = load_chats()

    if chat_id in chats:
        return chats[
            chat_id
        ].get(
            "files",
            []
        )
    return []


def auto_title(question):
    title = question.strip()

    if len(title) > 30:
        title = title[:30] + "..."

    return title