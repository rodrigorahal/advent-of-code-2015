import fileinput


def parse():
    return fileinput.input().readline().strip()


def destination(instructions):
    return sum(1 if char == "(" else -1 for char in instructions)


def basement(instructions):
    floor = 0
    for i, char in enumerate(instructions, start=1):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor == -1:
            return i


def main():
    instructions = parse()
    floor = destination(instructions)
    print(f"Part 1: {floor}")

    idx = basement(instructions)
    print(f"Part 2: {idx}")


if __name__ == "__main__":
    main()
