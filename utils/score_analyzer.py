def calculate_average(scores: list[int]) -> float:
    return sum(scores) / len(scores)


def get_passed_scores(scores: list[int]) -> list[int]:
    passed_scores: list[int] = []

    for score in scores:
        if score > 60:
            passed_scores.append(score)

    return passed_scores


def get_failed_scores(scores: list[int]) -> list[int]:
    failed_scores: list[int] = []

    for score in scores:
        if score < 60:
            failed_scores.append(score)

    return failed_scores


def get_max_score(scores: list[int]) -> int:
    return max(scores)


def get_min_score(scores: list[int]) -> int:
    return min(scores)