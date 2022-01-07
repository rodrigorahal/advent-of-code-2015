INPUT = "1113122113"


def step(digits):
    new_digits = []

    count = 1
    curr = digits[0]
    for nxt in digits[1:]:
        if curr == nxt:
            count += 1
        else:
            new_digits.append(str(count))
            new_digits.append(curr)
            count = 1
        curr = nxt

    new_digits.append(str(count))
    new_digits.append(curr)

    return "".join(new_digits)


def run(initial, steps=40):
    digits = initial
    for _ in range(steps):
        digits = step(digits)
    return digits


def main():
    digits = run(INPUT)
    print(f"Part 1: {len(digits)}")
    digits = run(INPUT, steps=50)
    print(f"Part 2: {len(digits)}")


if __name__ == "__main__":
    main()
