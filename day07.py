def calculate_average_score(students: list[dict[str, str | int]]) -> float:
    total_score: int = 0

    for student in students:
        score = student["score"]
        if isinstance(score, int):
            total_score += score

    return total_score / len(students)


def get_passed_students(
    students: list[dict[str, str | int]]
) -> list[dict[str, str | int]]:
    passed_students: list[dict[str, str | int]] = []

    for student in students:
        score = student["score"]
        if isinstance(score, int) and score >= 60:
            passed_students.append(student)

    return passed_students


def get_failed_students(
    students: list[dict[str, str | int]]
) -> list[dict[str, str | int]]:
    failed_students: list[dict[str, str | int]] = []

    for student in students:
        score = student["score"]
        if isinstance(score, int) and score < 60:
            failed_students.append(student)

    return failed_students


def get_top_student(students: list[dict[str, str | int]]) -> dict[str, str | int]:
    top_student: dict[str, str | int] = students[0]

    for student in students:
        score = student["score"]
        top_score = top_student["score"]

        if isinstance(score, int) and isinstance(top_score, int) and score > top_score:
            top_student = student

    return top_student


def print_student_report(students: list[dict[str, str | int]]) -> None:
    average_score: float = calculate_average_score(students)
    passed_students: list[dict[str, str | int]] = get_passed_students(students)
    failed_students: list[dict[str, str | int]] = get_failed_students(students)
    top_student: dict[str, str | int] = get_top_student(students)

    print(f"平均分：{average_score:.2f}")
    print(f"及格人数：{len(passed_students)}")
    print(f"不及格人数：{len(failed_students)}")
    print(f"最高分学生：{top_student['name']}，分数：{top_student['score']}")

    print("及格学生：")
    for student in passed_students:
        print(f"- {student['name']}：{student['score']}")

    print("不及格学生：")
    for student in failed_students:
        print(f"- {student['name']}：{student['score']}")


def main() -> None:
    students: list[dict[str, str | int]] = [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 82},
        {"name": "Charlie", "score": 67},
        {"name": "David", "score": 58},
        {"name": "Eva", "score": 43},
        {"name": "Frank", "score": 100},
        {"name": "Grace", "score": 76},
    ]

    print_student_report(students)


if __name__ == "__main__":
    main()