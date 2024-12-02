from pathlib import Path

import numpy as np


def main():
    input = Path("./input.txt").read_text()
    #      input = """
    #  3   4
    #  4   3
    #  2   5
    #  1   3
    #  3   9
    #  3   3
    #      """
    input = input.strip()
    lines = input.split("\n")
    x = [line.split() for line in lines]
    x = np.array(x, dtype=int)
    y = x[:, 0]
    z = x[:, 1]
    y.sort()
    z.sort()
    ans = np.abs((y - z)).sum()
    print(ans)

    ans2 = 0
    for a in y:
        ans2 += a * (z == a).sum()
    print(ans2)


if __name__ == "__main__":
    main()
