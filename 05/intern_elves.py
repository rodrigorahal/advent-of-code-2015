import fileinput
from collections import Counter, defaultdict
from itertools import pairwise, tee

BLOCKED = {"ab", "cd", "pq", "xy"}


def parse():
    words = []
    for line in fileinput.input():
        words.append(line.strip())
    return words


def triplewise(iterable):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def is_nice(word):
    return has_vowel_count(word) and has_twice_in_a_row(word) and not has_blocked(word)


def has_vowel_count(word):
    letter_counter = Counter(word)
    return sum(letter_counter[letter] for letter in "aeiou") >= 3


def has_twice_in_a_row(word):
    for a, b in pairwise(word):
        if a == b:
            return True
    return False


def has_blocked(word):
    for a, b in pairwise(word):
        if a + b in BLOCKED:
            return True
    return False


def is_nicer(word):
    return has_in_between(word) and has_pair_count(word)


def has_in_between(word):
    for a, b, c in triplewise(word):
        if a == c:
            return True
    return False


def has_pair_count(word):
    pair_idxs = defaultdict(set)
    for i, (a, b) in enumerate(pairwise(word)):
        pair_idxs[a + b].add(i)
        pair_idxs[a + b].add(i + 1)
    return any(len(idxs) >= 4 for idxs in pair_idxs.values())


def main():
    words = parse()
    print(f"Part 1: {sum(is_nice(word) for word in words)}")

    print(f"Part 2: {sum(is_nicer(word) for word in words)}")


if __name__ == "__main__":
    main()
