from itertools import pairwise, groupby

BLOCKED = {"i", "o", "l"}


def search(password):
    for candidate in increment(password):
        if is_valid(candidate):
            return candidate
    raise ValueError("not found")


def is_valid(password):
    return (
        has_increasing_three(password)
        and not has_blocked_letters(password)
        and has_non_overlapping_pairs(password)
    )


def increment(password):
    def propagate(current):
        current = current[:-1] + "a"
        carry = True
        i = -2
        while carry and i >= -8:
            letter = current[i]
            if ord(letter) + 1 <= 122:
                # break propagation
                carry = False
                current = current[:i] + chr(ord(letter) + 1) + current[i + 1 :]
            else:
                # keep propagating
                current = current[:i] + "a" + current[i + 1 :]
                i -= 1
        return current

    current = password
    while True:
        last = current[-1]
        if ord(last) + 1 > 122:
            current = propagate(current)
            yield current
        else:
            current = current[:-1] + chr(ord(last) + 1)
            yield current


def has_increasing_three(password):
    size = len(password)
    triplets = [
        [ord(letter) for letter in password[i : i + 3]] for i in range(size - 3)
    ]
    return any(snd == fst + 1 and trd == snd + 1 for fst, snd, trd in triplets)


def has_blocked_letters(password):
    return any(letter in BLOCKED for letter in password)


def has_non_overlapping_pairs(password):
    paired = set(letter for letter, group in groupby(password) if len(list(group)) > 1)
    return len(paired) > 1


def main():
    INPUT = "vzbxkghb"
    password = search(INPUT)
    print(f"Part 1: {password}")

    password = search(password)
    print(f"Part 2: {password}")


if __name__ == "__main__":
    main()
