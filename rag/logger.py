import pandas as pd
import os
from datetime import datetime


LOG_FILE = "logs/chat_logs.csv"

os.makedirs(
    "logs",
    exist_ok=True
)


def save_chat(
        question,
        answer
):

    new_data = pd.DataFrame(
        [
            {
                "timestamp": datetime.now(),
                "question": question,
                "answer": answer
            }
        ]
    )

    # File doesn't exist
    if not os.path.exists(
            LOG_FILE
    ):

        new_data.to_csv(
            LOG_FILE,
            index=False
        )

        return

    # File exists but is empty/corrupted
    try:

        old = pd.read_csv(
            LOG_FILE
        )

    except Exception:

        old = pd.DataFrame(
            columns=[
                "timestamp",
                "question",
                "answer"
            ]
        )

    updated = pd.concat(
        [old, new_data],
        ignore_index=True
    )

    updated.to_csv(
        LOG_FILE,
        index=False
    )