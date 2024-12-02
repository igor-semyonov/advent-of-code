from pathlib import Path

import numpy as np


def main():
    input = Path("./input.txt").read_text()
    if False:
        input = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
        """
    input = input.strip()
    lines = input.split("\n")

    safe = 0
    for row_idx, report in enumerate(lines):
        report = np.array(report.split(), dtype=int)
        a = report[:-1]
        b = report[1:]
        c = b - a
        d = np.abs(c).min()
        e = np.abs(c).max()
        if np.all(c > 0) or np.all(c < 0):
            if d >= 1 and e <= 3:
                #  print(row_idx, d, e)
                safe += 1

    print(safe)

    # part 2
    safe = 0
    for row_idx, report in enumerate(lines):
        report = np.array(report.split(), dtype=int)
        if test_report(report):
            safe += 1
            continue
        for idx in range(len(report)):
            if test_report(np.delete(report, idx)):
                safe += 1
                break

    print(safe)


def test_report(report: np.ndarray[int]) -> bool:
    a = report[:-1]
    b = report[1:]
    c = b - a
    d = np.abs(c).min()
    e = np.abs(c).max()
    if np.all(c > 0) or np.all(c < 0):
        if d >= 1 and e <= 3:
            #  print(row_idx, d, e)
            return True
    return False


if __name__ == "__main__":
    main()
