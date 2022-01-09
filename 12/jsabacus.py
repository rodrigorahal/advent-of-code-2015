import fileinput
import json


def parse():
    data = json.loads(fileinput.input().readline().strip())
    return data


def traverse(data, ignore_red=False):
    stack = [data]
    numbers = []

    while stack:
        token = stack.pop()

        if isinstance(token, int):
            numbers.append(token)

        if isinstance(token, dict):
            if ignore_red and any(v == "red" for v in token.values()):
                continue
            for v in token.values():
                stack.append(v)

        if isinstance(token, list):
            for item in token:
                stack.append(item)

    return numbers


def main():
    data = parse()
    numbers = traverse(data)
    print(f"Part 1: {sum(numbers)}")

    numbers = traverse(data, ignore_red=True)
    print(f"Part 2: {sum(numbers)}")


if __name__ == "__main__":
    main()
