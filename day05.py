def calculate_average(scores: list[int]) -> float:
    return sum(scores) / len(scores)


def get_passed_scores(scores: list[int]) -> list[int]:
    passed_scores: list[int] = []

    for score in scores:
        if score >= 60:
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


def main() -> None:
    scores: list[int] = [95, 82, 67, 58, 43, 100, 76]

    average_score: float = calculate_average(scores)
    passed_scores: list[int] = get_passed_scores(scores)
    failed_scores: list[int] = get_failed_scores(scores)
    max_score: int = get_max_score(scores)
    min_score: int = get_min_score(scores)

    print(f"平均分：{average_score}")
    print(f"最高分：{max_score}")
    print(f"最低分：{min_score}")
    print(f"及格分数：{passed_scores}")
    print(f"不及格分数：{failed_scores}")


if __name__ == "__main__":
    main()