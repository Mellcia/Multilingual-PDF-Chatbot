def calculate_confidence(
        distances
):

    if not distances:

        return 0

    score = (
        1 - (
            sum(distances)
            / len(distances)
        )
    )

    score = max(
        0,
        min(
            score,
            1
        )
    )

    return round(
        score * 100,
        2
    )