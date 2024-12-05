from pathlib import Path
from collections import defaultdict, deque
from itertools import permutations

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> str:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.read()
    return data


def parse_data(data: str) -> tuple[list[tuple[int]], list[list[int]]]:
    rules, updates = data.split("\n\n")
    rules = [tuple(map(int, y.strip().split("|"))) for y in rules.split("\n")]
    updates = [list(map(int, line.strip().split(","))) for line in updates.split("\n")]
    return rules, updates


def check_update(rule_set: set[tuple[int]], update: list[int]) -> bool:
    rev_update = update[::-1]
    wrong_updates = []
    for idx, val in enumerate(rev_update):
        for i in range(idx, len(rev_update)):
            if idx == i:
                continue
            wrong_updates.append((val, rev_update[i]))
    for wrong_update in wrong_updates:
        if wrong_update in rule_set:
            return False
    return True


def fix_update(rule_dict: dict[int, int], update: list[int]) -> list[int]:
    new_update = update.copy()
    fix = True
    while fix:
        fix = False
        for x in range(len(new_update)):
            if bad_vals := rule_dict[new_update[x]] & set(new_update[x:]):
                fix = True
                for val in bad_vals:
                    new_update.remove(val)
                    new_update.insert(0, val)
                break
    return new_update


def part1(rules: list[tuple[int]], updates: list[list[int]]) -> tuple[int, list[list[int]]]:
    rule_set = set(rules)
    valid_updates = []
    invalid_updates = []
    for update in updates:
        if check_update(rule_set, update):
            valid_updates.append(update)
        else:
            invalid_updates.append(update)
    return sum([i[len(i) // 2] for i in valid_updates]), invalid_updates


def part2(rules: list[tuple[int]], updates: list[list[int]]) -> int:
    rule_dict = defaultdict(set)
    for rule in rules:
        # reverse dict so vals should be infront of key
        rule_dict[rule[1]].add(rule[0])
    valid_updates = [fix_update(rule_dict, update) for update in updates]
    return sum([i[len(i) // 2] for i in valid_updates])


if __name__ == "__main__":
    input_str = get_input()
    rules, updates = parse_data(input_str)
    ans1, invalid_updates = part1(rules, updates)
    print(ans1)
    print(part2(rules, invalid_updates))
