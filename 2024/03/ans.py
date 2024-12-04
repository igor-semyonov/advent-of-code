import re
from pathlib import Path


def main():
    input = Path("./input.txt").read_text()
    if False:
        input = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
        """
    if False:  # part two
        input = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
        """
    input = input.strip()

    dos_and_donts = list(re.finditer("(do\\(\\)|don't\\(\\))", input))

    ans = 0
    for match in re.finditer("mul\\(\\d+,\\d+\\)", input):
        for do_or_dont in dos_and_donts[::-1]:
            if do_or_dont.start() < match.start():
                if input[do_or_dont.start() : do_or_dont.span()[1]] == "do()":
                    do = True
                else:
                    do = False
                break
        else:
            do = True
        if do:
            x, y = input[match.start() : match.span()[1]].strip("mul()").split(",")
            ans += int(x) * int(y)
    print(ans)


if __name__ == "__main__":
    main()
