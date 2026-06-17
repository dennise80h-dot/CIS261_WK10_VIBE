import unittest

from VIBE import Student, calculate_average, determine_grade


class StudentGradeCalculatorTests(unittest.TestCase):
    def test_calculate_average(self):
        student = Student("Jane", "S001", 85, 90, 95)
        self.assertEqual(calculate_average(student), 90.0)

    def test_determine_grade(self):
        self.assertEqual(determine_grade(95), "A")
        self.assertEqual(determine_grade(84), "B")
        self.assertEqual(determine_grade(71), "C")
        self.assertEqual(determine_grade(65), "D")
        self.assertEqual(determine_grade(59), "F")


if __name__ == "__main__":
    unittest.main()
