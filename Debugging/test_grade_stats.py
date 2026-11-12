"""Tests for grade_stats.py.  Run with:  pytest -v

Tip: these tests are deliberately small and focused. When one fails, its
NAME tells you which behavior is broken and its assertion tells you what
was expected vs. what you got.
"""
import pytest

from grade_stats import (
    add_score,
    average,
    curve,
    letter_grade,
    median,
    top_students,
)


# ---------- add_score ----------

def test_add_score_creates_new_book():
    book = add_score("ana", 90)
    assert book == {"ana": [90]}


def test_add_score_appends_to_existing_student():
    book = {"ana": [90]}
    add_score("ana", 80, book)
    assert book == {"ana": [90, 80]}


def test_add_score_new_book_is_independent_of_earlier_calls():
    first = add_score("ana", 90)
    second = add_score("ben", 70)
    assert "ben" not in first
    assert second == {"ben": [70]}


# ---------- average ----------

def test_average_empty_is_zero():
    assert average([]) == 0.0


def test_average_exact():
    assert average([80, 90]) == 85.0


def test_average_fractional():
    assert average([89, 90]) == pytest.approx(89.5)


# ---------- median ----------

def test_median_odd_length():
    assert median([5, 1, 3]) == 3


def test_median_even_length():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_two_items():
    assert median([10, 20]) == 15


# ---------- letter_grade ----------

@pytest.mark.parametrize(
    "avg, expected",
    [(95, "A"), (85, "B"), (75, "C"), (65, "D"), (30, "F")],
)
def test_letter_grade_typical(avg, expected):
    assert letter_grade(avg) == expected


@pytest.mark.parametrize(
    "avg, expected",
    [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (59.9, "F")],
)
def test_letter_grade_boundaries(avg, expected):
    assert letter_grade(avg) == expected


# ---------- curve ----------

def test_curve_adds_bonus_and_caps_at_100():
    assert curve([70, 98], 5) == [75, 100]


def test_curve_does_not_modify_input():
    original = [70, 98]
    curve(original, 5)
    assert original == [70, 98]


# ---------- top_students ----------

def test_top_students_best_first():
    book = {"ana": [90, 100], "ben": [60, 70], "cy": [80, 85]}
    assert top_students(book, 2) == ["ana", "cy"]


def test_top_students_n_larger_than_class():
    book = {"ana": [90], "ben": [60]}
    assert top_students(book, 5) == ["ana", "ben"]


def test_top_students_close_averages():
    # ana averages 89.5, ben averages 89.0 -- ana should win.
    book = {"ben": [89, 89], "ana": [89, 90]}
    assert top_students(book, 1) == ["ana"]
