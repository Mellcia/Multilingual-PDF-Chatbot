MAX_HISTORY = 5


def get_chat_context(messages):

    history = []

    for msg in messages[-MAX_HISTORY:]:

        role = msg["role"]

        content = msg["content"]

        history.append(
            f"{role}: {content}"
        )

    return "\n".join(history)