"""
INSTRUCTOR ANSWER KEY: one reasonable refactoring (not the only one).

Design choices worth discussing with students:
* letter_grade() is a FUNCTION: input in, answer out, no memory needed.
* parse_row() is a FUNCTION: one job, turns text into values.
* Student is a CLASS: it bundles related data (name, scores) with the
  calculations that belong to that data (hw_avg, score, letter).
* Globals are gone: counts are derived from the list of students, so
  calling main() twice gives the same output.
"""
import sys
 
RAW_DATA = """name,hw1,hw2,hw3,midterm,final
Ada,90,85,100,88,92
Grace,78,82,80,75,85
Linus,55,60,48,62,58
Margaret,100,95,98,99,97
Alan,70,,65,72,68
Barbara,88,91,85,79,90
Dennis,45,50,52,40,47
"""

HW_WEIGHT = 0.3
MIDTERM_WEIGHT = 0.3
FINAL_WEIGHT = 0.4
GRADE_CUTOFFS = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]


def letter_grade(score):
    for cutoff, letter in GRADE_CUTOFFS:
        if score >= cutoff:
            return letter
    return "F"


class Student:
    def __init__(self, name, homework, midterm, final):
        self.name = name
        self.homework = homework
        self.midterm = midterm
        self.final = final

    @property
    def hw_avg(self):
        return sum(self.homework) / len(self.homework)

    @property
    def score(self):
        return (
            self.hw_avg * HW_WEIGHT
            + self.midterm * MIDTERM_WEIGHT
            + self.final * FINAL_WEIGHT
        )

    @property
    def letter(self):
        return letter_grade(self.score)


def to_int(text):
    return int(text) if text != "" else 0


def parse_row(line):
    parts = line.split(",")
    return Student(
        name=parts[0],
        homework=[to_int(p) for p in parts[1:4]],
        midterm=to_int(parts[4]),
        final=to_int(parts[5]),
    )


def load_students(data):
    lines = data.strip().split("\n")
    return [parse_row(line) for line in lines[1:]]


def print_report(students):
    print("=== Grade Report ===")
    for s in students:
        print(
            f"{s.name:<10} HW {s.hw_avg:5.1f}  Mid {s.midterm:3d}  "
            f"Final {s.final:3d}  Score {s.score:5.1f}  {s.letter}"
        )


def print_curved_report(students, curve):
    print(f"=== Curved Report (+{curve}) ===")
    for s in students:
        new_score = min(s.score + curve, 100)
        print(f"{s.name:<10} Score {new_score:5.1f}  {letter_grade(new_score)}")


def print_summary(students):
    scores = [s.score for s in students]
    best = max(students, key=lambda s: s.score)
    worst = min(students, key=lambda s: s.score)
    print("=== Summary ===")
    print(f"Students: {len(students)}")
    print(f"Class average: {sum(scores) / len(scores):.1f}")
    print(f"Highest: {best.name} ({best.score:.1f})")
    print(f"Lowest: {worst.name} ({worst.score:.1f})")
    print("Grade distribution:")
    for _, letter in GRADE_CUTOFFS + [(0, "F")]:
        count = sum(1 for s in students if s.letter == letter)
        print(f"  {letter}: {'#' * count}")


def main():
    students = load_students(RAW_DATA)
    print_report(students)
    print()
    print_curved_report(students, 5)
    print()
    print_summary(students)


EXPECTED_OUTPUT = """=== Grade Report ===
Ada        HW  91.7  Mid  88  Final  92  Score  90.7  A
Grace      HW  80.0  Mid  75  Final  85  Score  80.5  B
Linus      HW  54.3  Mid  62  Final  58  Score  58.1  F
Margaret   HW  97.7  Mid  99  Final  97  Score  97.8  A
Alan       HW  45.0  Mid  72  Final  68  Score  62.3  D
Barbara    HW  88.0  Mid  79  Final  90  Score  86.1  B
Dennis     HW  49.0  Mid  40  Final  47  Score  45.5  F

=== Curved Report (+5) ===
Ada        Score  95.7  A
Grace      Score  85.5  B
Linus      Score  63.1  D
Margaret   Score 100.0  A
Alan       Score  67.3  D
Barbara    Score  91.1  A
Dennis     Score  50.5  F

=== Summary ===
Students: 7
Class average: 74.4
Highest: Margaret (97.8)
Lowest: Dennis (45.5)
Grade distribution:
  A: ##
  B: ##
  C: 
  D: #
  F: ##
"""


def check():
    import contextlib
    import io

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        main()
    print("PASS" if buffer.getvalue() == EXPECTED_OUTPUT else "FAIL")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        main()
