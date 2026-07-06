students = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 82},
    {"name": "Cindy", "score": 58},
    {"name": "David", "score": 43},
    {"name": "Eva", "score": 76},
]


def get_average_score(students: list[dict[str, int | str]]) -> float:
    if len(students) == 0:
        return 0
    total_score = 0
    for student in students:
        total_score += student["score"]
    average_score = total_score / len(students)
    return average_score


def get_passed_students(students: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    if len(students) == 0:
        return []
    passed_students = []
    for student in students:
        if student["score"] >= 60:
            passed_students.append(student)
    return passed_students


def get_failed_students(students: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    if len(students) == 0:
        return []
    failed_students = []
    for student in students:
        if student["score"] < 60:
            failed_students.append(student)
    return failed_students


def print_main_info(
    students: list[dict[str, int | str]],
    passed_students: list[dict[str, int | str]],
    failed_students: list[dict[str, int | str]]
) -> None:
    print(f"学生总数：{len(students)}")
    print(f"平均分：{get_average_score(students)}")
    print(f"通过人数：{len(passed_students)}")
    print(f"未通过人数：{len(failed_students)}")


def print_passed_students(passed_students: list[dict[str, int | str]]) -> None:
    print(f"\n通过学生：")
    for student in passed_students:
        print(f"{student['name']} - {student['score']}")


def print_failed_students(failed_students: list[dict[str, int | str]]) -> None:
    print(f"\n未通过学生：")
    for student in failed_students:
        print(f"{student['name']} - {student['score']}")


def main() -> None:
    passed_students = get_passed_students(students)
    failed_students = get_failed_students(students)

    print_main_info(students, passed_students, failed_students)
    print_passed_students(passed_students)
    print_failed_students(failed_students)


if __name__ == "__main__":
    main()
