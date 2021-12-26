import fileinput
from collections import Counter


def parse():
    return fileinput.input().readline().strip()


def deliver(directions, with_robot=False):
    start = (0, 0)
    houses = Counter({start: 1})
    movers = [(0, 0), (0, 0)]
    for i, dir in enumerate(directions):
        if with_robot:
            to_move_idx = i % 2
        else:
            to_move_idx = 0
        loc = movers[to_move_idx]
        x, y = loc
        if dir == "^":
            loc = (x, y + 1)
        if dir == "v":
            loc = (x, y - 1)
        if dir == ">":
            loc = (x + 1, y)
        if dir == "<":
            loc = (x - 1, y)
        houses[loc] += 1
        movers[to_move_idx] = loc
    return houses


def main():
    directions = parse()
    houses = deliver(directions)
    print(f"Part 1: {len(houses)}")

    houses = deliver(directions, with_robot=True)
    print(f"Part 2: {len(houses)}")


if __name__ == "__main__":
    main()
