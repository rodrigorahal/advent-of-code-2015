import fileinput
import math
from itertools import combinations
import numbers
from tokenize import group


def parse():
    return [int(line.strip()) for line in fileinput.input()]


def candidate_partitions(numbers, size):
    candidates = []
    for first_size in range(2, len(numbers)):
        if len(candidates) > 0:
            break
        for first in combinations(numbers, first_size):
            remaining = [a for a in numbers if a not in first]
            if sum(first) * (size - 1) == sum(remaining):
                candidates.append((first, remaining))
    return sorted(candidates, key=entaglement)


def search(candidates, size):
    for candidate in candidates:
        if can_be_partitioned(candidate, size):
            return candidate


def can_be_partitioned(candidate, size):
    first, remaining = candidate
    target = sum(first)

    for r in range(2, len(remaining)):
        for nxt_group in combinations(remaining, r):
            if sum(nxt_group) != target:
                continue
            still_remaining = set(remaining) - set(nxt_group)
            if size == 3 and sum(still_remaining) == target:
                return True
            elif size == 4 and can_be_partitioned((first, still_remaining), 3):
                return True
    return False


def entaglement(candidate):
    fst, _ = candidate
    return math.prod(fst)


def main():
    numbers = parse()
    candidates = candidate_partitions(numbers, 3)
    candidate = search(candidates, 3)
    print(f"Part 1: {entaglement(candidate)}")

    candidates = candidate_partitions(numbers, 4)
    candidate = search(candidates, 4)
    print(f"Part 2: {entaglement(candidate)}")


if __name__ == "__main__":
    main()
