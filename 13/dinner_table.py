import fileinput
from collections import defaultdict
from itertools import permutations


def parse():
    people = set()
    happiness = defaultdict(int)

    for line in fileinput.input():
        words = line.strip().strip(".").split(" ")
        pair = words[0], words[-1]
        sign, ammount = 1 if words[2] == "gain" else -1, int(words[3])
        happiness[pair] = sign * ammount
        people.update(pair)

    return list(people), happiness


def search(people, happiness):
    return [
        (score(arrangement, happiness), arrangement)
        for arrangement in permutations(people)
    ]


def score(arrangement, happiness):
    level = 0

    n = len(arrangement)
    for i in range(len(arrangement)):
        prev, curr, nxt = (
            arrangement[i - 1],
            arrangement[i],
            arrangement[(i + 1) % n],
        )
        level += happiness[(curr, prev)]
        level += happiness[(curr, nxt)]
    return level


def main():
    people, happiness = parse()
    scores = search(people, happiness)
    print(f"Part 1: {max(scores)}")

    you = "You"
    for person in people:
        happiness[(you, person)] = 0
        happiness[(person, you)] = 0
    people.append(you)
    scores = search(people, happiness)
    print(f"Part 2: {max(scores)}")


if __name__ == "__main__":
    main()
