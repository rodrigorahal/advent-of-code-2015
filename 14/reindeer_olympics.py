import fileinput
from collections import defaultdict
from operator import itemgetter


def parse():
    reindeer = []
    for line in fileinput.input():
        words = line.strip().strip(".").split(" ")
        name = words[0]
        speed = int(words[3])
        fly = int(words[6])
        rest = int(words[-2])
        cycle = fly + rest
        reindeer.append((name, speed, fly, rest, cycle))
    return reindeer


def compete(reindeer, time):
    return max([race(rndr, time) for rndr in reindeer], key=itemgetter(1))


def race(reindeer, time):
    traveled = 0

    name, speed, fly, rest, cycle = reindeer

    full_cycles = time // cycle
    remaining = time % cycle

    traveled += full_cycles * fly * speed
    traveled += min(remaining, fly) * speed

    return name, traveled


def simulate(reindeer, time):
    scores = defaultdict(int)
    positions = defaultdict(int)

    for step in range(1, time + 1):
        for rndr in reindeer:
            name, traveled = race(rndr, step)
            positions[name] = traveled

        winners = [
            name for name, pos in positions.items() if pos == max(positions.values())
        ]
        for winner in winners:
            scores[winner] += 1
    return max([(name, score) for name, score in scores.items()], key=itemgetter(1))


def main():
    reindeer = parse()
    print(f"Part 1: {compete(reindeer, 2503)}")
    print(f"Part 2: {simulate(reindeer, 2503)}")


if __name__ == "__main__":
    main()
