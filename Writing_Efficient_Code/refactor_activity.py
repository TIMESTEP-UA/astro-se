"""
REFACTORING ACTIVITY  (20 minutes, work in pairs)
 
This program prints a grade report for a small class. It WORKS, but it is
hard to read, hard to change, and hard to test.

Your job: refactor it so a new teammate could understand and extend it,
WITHOUT changing what it prints. You decide what is wrong and how to fix it.

Setup:   python refactor_activity.py          (see the report)
Check:   python refactor_activity.py --check  (does your output still match?)

Run --check after every change. If it fails, undo your last change.

Be ready to explain: what did you turn into functions, what into classes,
and why? What would you do next if you had another 20 minutes?

If you finish early:
* Call main() twice in a row. Is the output identical? Why or why not?
* Split the code into modules and import them.
* Write pytest tests for the pieces you extracted.
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

total_students = 0
grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}


def process(data):
    global total_students
    lines = data.strip().split("\n")
    results = []
    for line in lines[1:]:
        parts = line.split(",")
        name = parts[0]
        hw1 = int(parts[1]) if parts[1] != "" else 0
        hw2 = int(parts[2]) if parts[2] != "" else 0
        hw3 = int(parts[3]) if parts[3] != "" else 0
        midterm = int(parts[4]) if parts[4] != "" else 0
        final = int(parts[5]) if parts[5] != "" else 0
        hw_avg = (hw1 + hw2 + hw3) / 3
        score = hw_avg * 0.3 + midterm * 0.3 + final * 0.4
        if score >= 90:
            letter = "A"
        elif score >= 80:
            letter = "B"
        elif score >= 70:
            letter = "C"
        elif score >= 60:
            letter = "D"
        else:
            letter = "F"
        grade_counts[letter] += 1
        total_students += 1
        results.append((name, hw_avg, midterm, final, score, letter))
    return results


def print_report(results):
    print("=== Grade Report ===")
    for r in results:
        print(
            f"{r[0]:<10} HW {r[1]:5.1f}  Mid {r[2]:3d}  "
            f"Final {r[3]:3d}  Score {r[4]:5.1f}  {r[5]}"
        )


def print_curved_report(results, curve):
    print(f"=== Curved Report (+{curve}) ===")
    for r in results:
        new_score = r[4] + curve
        if new_score > 100:
            new_score = 100
        if new_score >= 90:
            letter = "A"
        elif new_score >= 80:
            letter = "B"
        elif new_score >= 70:
            letter = "C"
        elif new_score >= 60:
            letter = "D"
        else:
            letter = "F"
        print(f"{r[0]:<10} Score {new_score:5.1f}  {letter}")


def print_summary(results):
    scores = [r[4] for r in results]
    print("=== Summary ===")
    print(f"Students: {total_students}")
    print(f"Class average: {sum(scores) / len(scores):.1f}")
    best = results[0]
    worst = results[0]
    for r in results:
        if r[4] > best[4]:
            best = r
        if r[4] < worst[4]:
            worst = r
    print(f"Highest: {best[0]} ({best[4]:.1f})")
    print(f"Lowest: {worst[0]} ({worst[4]:.1f})")
    print("Grade distribution:")
    for letter in grade_counts:
        print(f"  {letter}: {'#' * grade_counts[letter]}")


def main():
    results = process(RAW_DATA)
    print_report(results)
    print()
    print_curved_report(results, 5)
    print()
    print_summary(results)


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
    if buffer.getvalue() == EXPECTED_OUTPUT:
        print("PASS: output matches. Nice work!")
    else:
        print("FAIL: output changed. Compare yours to this expected output:")
        print(EXPECTED_OUTPUT)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        main()
