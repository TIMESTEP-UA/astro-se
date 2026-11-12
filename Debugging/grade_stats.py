"""grade_stats.py -- small gradebook utilities.

A *gradebook* is a dict that maps each student's name (str) to a list of that
student's scores (a list of int or float values, normally between 0 and 100):

    {"ana": [90, 100], "ben": [60, 70]}

STUDENT VERSION: this file contains bugs. Do not read ahead for them;
let the tests and the debugger lead you to them.
"""


def add_score(name, score, book={}):
    """Record one score for a student and return the gradebook.

    Args:
        name (str): The student's name. If the student is not in the
            gradebook yet, they are added with an empty score list first.
        score (int or float): The score to append to that student's list.
        book (dict, optional): An existing gradebook (name -> list of scores)
            to add to. If omitted, a brand-new, empty gradebook is started
            for this call; separate calls must never share one.

    Returns:
        dict: The gradebook containing the new score. When `book` is passed
        in, this is that same dict, modified in place.

    Examples:
        >>> add_score("ana", 90)
        {'ana': [90]}
        >>> book = {"ana": [90]}
        >>> add_score("ana", 80, book)
        {'ana': [90, 80]}
    """
    book.setdefault(name, []).append(score)
    return book


def average(scores):
    """Return the arithmetic mean of a list of scores.

    Args:
        scores (list of int or float): The scores to average. May be empty.

    Returns:
        float: The sum of the scores divided by how many there are, as a
        true (not rounded or truncated) mean. Returns 0.0 for an empty list.

    Examples:
        >>> average([80, 90])
        85.0
        >>> average([89, 90])
        89.5
        >>> average([])
        0.0
    """
    if not scores:
        return 0.0
    return sum(scores) // len(scores)


def median(scores):
    """Return the median (middle value) of a list of scores.

    Args:
        scores (list of int or float): The scores, in any order. May be
            empty. The list is not modified.

    Returns:
        int or float: With an odd number of scores, the middle score once
        sorted. With an even number, the mean of the two middle scores.
        Returns 0.0 for an empty list.

    Examples:
        >>> median([5, 1, 3])
        3
        >>> median([1, 2, 3, 4])
        2.5
        >>> median([10, 20])
        15.0
        >>> median([])
        0.0
    """
    if not scores:
        return 0.0
    ordered = sorted(scores)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 0:
        return (ordered[mid - 1] + ordered[mid + 1]) / 2
    return ordered[mid]


def letter_grade(avg):
    """Convert a numeric average to a letter grade.

    Args:
        avg (int or float): The numeric average, normally 0 to 100.

    Returns:
        str: One of "A", "B", "C", "D" or "F", using these cutoffs, where
        each lower bound is included in its grade:

            90 or higher -> "A"
            80 or higher -> "B"
            70 or higher -> "C"
            60 or higher -> "D"
            below 60     -> "F"

    Examples:
        >>> letter_grade(95)
        'A'
        >>> letter_grade(90)
        'A'
        >>> letter_grade(59.9)
        'F'
    """
    if avg > 90:
        return "A"
    elif avg > 80:
        return "B"
    elif avg > 70:
        return "C"
    elif avg > 60:
        return "D"
    return "F"


def curve(scores, bonus):
    """Add a bonus to every score, never letting a score exceed 100.

    Args:
        scores (list of int or float): The original scores. This list must
            not be modified.
        bonus (int or float): The number of points to add to each score.

    Returns:
        list: A NEW list, the same length and order as `scores`, where each
        entry is the original score plus `bonus`, capped at 100.

    Examples:
        >>> original = [70, 98]
        >>> curve(original, 5)
        [75, 100]
        >>> original
        [70, 98]
    """
    for i in range(len(scores)):
        scores[i] = min(scores[i] + bonus, 100)
    return scores


def top_students(book, n):
    """Return the names of the students with the highest averages.

    Args:
        book (dict): A gradebook mapping each student's name (str) to a list
            of their scores. A student with an empty list has an average
            of 0.0 (see `average`).
        n (int): The maximum number of names to return.

    Returns:
        list of str: Up to `n` student names, ordered from highest average
        to lowest. If `n` is larger than the number of students, every
        student is returned. The order of students with equal averages is
        not specified.

    Examples:
        >>> book = {"ana": [90, 100], "ben": [60, 70], "cy": [80, 85]}
        >>> top_students(book, 2)
        ['ana', 'cy']
    """
    ranked = sorted(book, key=lambda name: average(book[name]))
    return ranked[:n]
