import fileinput
from collections import defaultdict


def parse():
    instructions = []
    for line in fileinput.input():
        words = line.strip().split(" ")
        if line.startswith("toggle"):
            xlo, ylo = tuple(map(int, words[1].split(",")))
            xhi, yhi = tuple(map(int, words[3].split(",")))
            instructions.append(("toggle", xlo, ylo, xhi, yhi))
        else:
            xlo, ylo = tuple(map(int, words[2].split(",")))
            xhi, yhi = tuple(map(int, words[4].split(",")))
            cmd = words[1]
            instructions.append((cmd, xlo, ylo, xhi, yhi))
    return instructions


def follow(instructions):
    on = set()
    for cmd, xlo, ylo, xhi, yhi in instructions:
        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                if cmd == "on" or (cmd == "toggle" and (x, y) not in on):
                    on.add((x, y))
                elif cmd == "off" or (cmd == "toggle" and (x, y) in on):
                    on.discard((x, y))
    return on


def follow_with_brightness(instructions):
    brightness = defaultdict(int)
    for cmd, xlo, ylo, xhi, yhi in instructions:
        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                if cmd == "on":
                    brightness[(x, y)] += 1
                if cmd == "off":
                    brightness[(x, y)] = max(brightness[(x, y)] - 1, 0)
                if cmd == "toggle":
                    brightness[(x, y)] += 2
    return brightness


def main():
    instructions = parse()
    on = follow(instructions)
    print(f"Part 1: {len(on)}")
    brightness = follow_with_brightness(instructions)
    print(f"Part 2: {sum(brightness.values())}")


if __name__ == "__main__":
    main()
