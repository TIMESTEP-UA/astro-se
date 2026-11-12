"""
Run it normally first:        python demo_pdb.py
Then debug it:                python -m pdb demo_pdb.py
"""


def longest_run(items):
    """Return the length of the longest streak of equal adjacent items.

    longest_run([1, 1, 2, 2, 2, 3]) -> 3
    longest_run([]) -> 0
    """
    if not items:
        return 0

    best = 1
    current = 1
    for i in range(1, len(items)): 
        if items[i] == items[i - 1]:
            current += 1
        else:
            best = max(best, current)
            current = 1
    return max(best, current)


def main():
    examples = [
        ([], 0),
        ([7], 1),
        ([1, 1, 2, 2, 2, 3], 3),   # streak in the middle: works
        ([1, 2, 2, 2], 3),          # streak at the END: fails
    ]
    for data, expected in examples:
        got = longest_run(data)
        status = "ok " if got == expected else "BUG"
        print(f"{status} longest_run({data}) = {got}, expected {expected}")


if __name__ == "__main__":
    main()
