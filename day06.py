from utils.score_analyzer import (
    calculate_average,
    get_failed_scores,
    get_max_score,
    get_min_score,
    get_passed_scores
)

def print_scores_report(scores: list[int]) -> None:
    average_score: float = calculate_average(scores)
    passed_scores: list[int] = get_passed_scores(scores)
    failed_scores: list[int] = get_failed_scores(scores)
    max_score: int = get_max_score(passed_scores)
    min_score: int = get_min_score(passed_scores)

    print("成绩分析报告")
    print(f"全部成绩：{scores}")
    print(f"平均分：{average_score:.2f}")
    print(f"及格成绩：{passed_scores}")
    print(f"不及格成绩：{failed_scores}")
    print(f"最高分：{max_score}")
    print(f"最低分：{min_score}")


def main() -> None:
    scores: list[int] = [95, 82, 67, 58, 43, 100, 76]

    print_scores_report(scores)


if __name__ == "__main__":
    main()