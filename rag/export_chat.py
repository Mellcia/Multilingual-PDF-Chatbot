def export_chat(messages):

    chat = ""

    for message in messages:

        role = message["role"]

        content = message["content"]

        chat += (
            f"{role.upper()}:\n"
        )

        chat += (
            f"{content}\n\n"
        )

    return chat