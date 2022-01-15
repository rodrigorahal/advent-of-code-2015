import fileinput
from itertools import combinations


def parse():
    return [int(line.strip()) for line in fileinput.input()]


def search(containers, target, with_minimum=False):
    count = 0
    n = len(containers)
    for r in range(1, n):
        for group in combinations(containers, r):
            if sum(group) == target:
                count += 1
        if with_minimum and count:
            break
    return count


def main():
    TARGET = 150
    containers = parse()
    print(f"Part 1: {search(containers, TARGET)}")
    print(f"Part 2 {search(containers, TARGET, with_minimum=True)}")


if __name__ == "__main__":
    main()
