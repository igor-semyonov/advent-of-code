import re
from pathlib import Path

import numpy as np


def main():
    input = Path("./input.txt").read_text()
    if False:
        input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
        """
    input = input.strip()
    rules, updates = input.split("\n\n")
    rules = rules.strip()
    rules = [
        [int(x) for x in rule.split("|")] for rule in rules.split()
    ]
    updates = [
        [int(x) for x in update.split(",")]
        for update in updates.split()
    ]

    ans = 0
    for update in updates:
        for rule in rules:
            x, y = rule
            if x not in update or y not in update:
                continue

            idx_x = update.index(x)
            idx_y = update.index(y)

            if idx_y < idx_x:
                break
        else:
            ans += update[int(len(update) / 2)]

    print(ans)

    # part 2
    ans = 0
    flagged_updates_idx = []
    for idx_update, update in enumerate(updates):
        while True:
            for rule in rules:
                x, y = rule
                if x not in update or y not in update:
                    continue

                idx_x = update.index(x)
                idx_y = update.index(y)

                if idx_y < idx_x:
                    update[idx_x], update[idx_y] = y, x
                    flagged_updates_idx.append(idx_update)
                    break
            else:
                break

    for idx in set(flagged_updates_idx):
        update = updates[idx]
        ans += update[int(len(update) / 2)]
    print(ans)


if __name__ == "__main__":
    main()
