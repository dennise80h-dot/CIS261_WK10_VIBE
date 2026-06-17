from dataclasses import dataclass
from pathlib import Path
from typing import List

FILE_NAME = "student_grades.txt"


@dataclass
class Student:
    name: str
    id: str
    test1: float
    test2: float
    test3: float
    average: float = 0.0
    grade: str = ""

    def __post_init__(self):
        self.average = calculate_average(self)
        self.grade = determine_grade(self.average)


def calculate_average(student: Student) -> float:
    return round((student.test1 + student.test2 + student.test3) / 3, 2)


def determine_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def get_valid_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print("Please enter a valid numeric score.")


def load_students(file_name: str = FILE_NAME) -> List[Student]:
    students: List[Student] = []
    try:
        path = Path(file_name)
        if not path.exists():
            return students

        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print("Skipping invalid record:")
                    print(f"  {line}")
                    continue

                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    student = Student(
                        name=name,
                        id=student_id,
                        test1=float(test1),
                        test2=float(test2),
                        test3=float(test3),
                    )
                    student.average = float(average)
                    student.grade = grade
                    students.append(student)
                except ValueError:
                    print(f"Could not read record for {name}.")
    except OSError as error:
        print(f"Error reading file: {error}")

    return students


def save_students(students: List[Student], file_name: str = FILE_NAME) -> None:
    try:
        with Path(file_name).open("w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student.name}|{student.id}|{student.test1:.2f}|{student.test2:.2f}|{student.test3:.2f}|"
                    f"{student.average:.2f}|{student.grade}\n"
                )
        print(f"Records saved to {file_name}.")
    except OSError as error:
        print(f"Error saving file: {error}")


def add_student(students: List[Student]) -> None:
    print("\nAdd a new student")
    name = input("Enter student name: ").strip()
    student_id = input("Enter student ID: ").strip()

    if not name or not student_id:
        print("Name and ID are required.")
        return

    test1 = get_valid_float("Enter Test 1 score: ")
    test2 = get_valid_float("Enter Test 2 score: ")
    test3 = get_valid_float("Enter Test 3 score: ")

    student = Student(name=name, id=student_id, test1=test1, test2=test2, test3=test3)
    students.append(student)
    print(f"Student {name} added successfully.")


def display_students(students: List[Student]) -> None:
    if not students:
        print("No student records to display.")
        return

    print("\nStudent Records")
    print(
        f"{'Name':<15} {'ID':<8} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Avg':>8} {'Grade':>6}"
    )
    print("-" * 70)
    for student in students:
        print(
            f"{student.name:<15} {student.id:<8} "
            f"{student.test1:>8.2f} {student.test2:>8.2f} {student.test3:>8.2f} "
            f"{student.average:>8.2f} {student.grade:>6}"
        )


def search_student(students: List[Student]) -> None:
    name = input("Enter student name to search: ").strip()
    matches = [student for student in students if name.lower() in student.name.lower()]

    if not matches:
        print(f"No student found matching '{name}'.")
        return

    print(f"\nSearch results for '{name}':")
    for student in matches:
        print(
            f"{student.name} ({student.id}) - Avg: {student.average:.2f}, Grade: {student.grade}"
        )


def display_class_statistics(students: List[Student]) -> None:
    if not students:
        print("No student records available for statistics.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average:  {lowest:.2f}")
    print(f"Class Average:   {class_average:.2f}")


def main() -> None:
    students = load_students()
    print("Welcome to the Student Grade Calculator")
    print("Type ESC at the menu to exit.\n")

    while True:
        print("Menu")
        print("1. Add student")
        print("2. Display all students")
        print("3. Search student")
        print("4. Class statistics")
        print("5. Save records")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice.upper() == "ESC" or choice == "6":
            save_students(students)
            print("Program ended.")
            break
        elif choice == "1":
            add_student(students)
            save_students(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            display_class_statistics(students)
        elif choice == "5":
            save_students(students)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

