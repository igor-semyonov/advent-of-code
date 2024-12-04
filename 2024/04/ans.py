import re
from pathlib import Path

import numpy as np


def main():
    input = Path("./input.txt").read_text()
    if False:
        input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
        """
    input = input.strip()
    lines = input.split("\n")
    arr = np.array([list(line) for line in lines])
    Xs = np.where(arr == "X")
    ans = 0
    z = np.exp(1j * 2 * np.pi * np.linspace(0, 7 / 8, 8))
    x = np.round(z.real).astype(int).tolist()
    y = np.round(z.imag).astype(int).tolist()
    for r, c in zip(*Xs):
        for direction in zip(y, x):
            for i, next_char in enumerate(list("MAS")):
                next_row = r + (i + 1) * direction[0]
                next_col = c + (i + 1) * direction[1]
                if next_col >= arr.shape[1] or next_col < 0:
                    break
                if next_row >= arr.shape[0] or next_row < 0:
                    break
                if arr[next_row, next_col] != next_char:
                    break
            else:
                ans += 1
    print(ans)

    # part 2
    As = np.where(arr == "A")
    n_row, n_col = arr.shape
    ans = 0
    for r, c in zip(*As):
        if r == 0 or r == n_row - 1 or c == 0 or c == n_col - 1:
            continue
        if (
            (arr[r - 1, c - 1] == "M" and arr[r + 1, c + 1] == "S")
            or (arr[r - 1, c - 1] == "S" and arr[r + 1, c + 1] == "M")
        ) and (
            (arr[r + 1, c - 1] == "M" and arr[r - 1, c + 1] == "S")
            or (arr[r + 1, c - 1] == "S" and arr[r - 1, c + 1] == "M")
        ):
            ans += 1
    print(ans)


if __name__ == "__main__":
    main()
