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


def follow_with_compression(instructions):
    X, Y = coordinates(instructions)
    x_compressed, x_len_by_compressed = compress(X)
    y_compressed, y_len_by_compressed = compress(Y)

    on = set()
    for cmd, xlo, ylo, xhi, yhi in instructions:
        for xcomp in range(x_compressed[xlo], x_compressed[xhi + 1]):
            for ycomp in range(y_compressed[ylo], y_compressed[yhi + 1]):
                if cmd == "on" or (cmd == "toggle" and (xcomp, ycomp) not in on):
                    on.add((xcomp, ycomp))
                elif cmd == "off" or (cmd == "toggle" and (xcomp, ycomp) in on):
                    on.discard((xcomp, ycomp))

    lights_on = 0
    for xcomp, ycomp in on:
        lights_on += x_len_by_compressed[xcomp] * y_len_by_compressed[ycomp]
    return lights_on


def coordinates(instructions):
    X = set()
    Y = set()
    for _, xlo, ylo, xhi, yhi in instructions:
        X.add(xlo)
        X.add(xhi + 1)
        Y.add(ylo)
        Y.add(yhi + 1)
    return X, Y


def compress(coordinates):
    sorted_coordinates = sorted(c for c in coordinates)
    compressed = {}
    length_by_compressed = {}
    for i, coordinate in enumerate(sorted_coordinates):
        compressed[coordinate] = i
        if i > len(coordinates) - 2:
            continue
        else:
            length_by_compressed[i] = sorted_coordinates[i + 1] - coordinate
    return compressed, length_by_compressed


def follow_for_brightness(instructions):
    brightness = defaultdict(int)
    for cmd, xlo, ylo, xhi, yhi in instructions:
        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                if cmd == "on":
                    brightness[(x, y)] += 1
                elif cmd == "off":
                    brightness[(x, y)] = max(brightness[(x, y)] - 1, 0)
                elif cmd == "toggle":
                    brightness[(x, y)] += 2
    return brightness


def follow_for_brightness_with_compression(instructions):
    X, Y = coordinates(instructions)
    x_compressed, x_len_by_compressed = compress(X)
    y_compressed, y_len_by_compressed = compress(Y)

    brightness = defaultdict(int)
    for cmd, xlo, ylo, xhi, yhi in instructions:
        for xcomp in range(x_compressed[xlo], x_compressed[xhi + 1]):
            for ycomp in range(y_compressed[ylo], y_compressed[yhi + 1]):
                if cmd == "on":
                    brightness[(xcomp, ycomp)] += 1
                elif cmd == "off":
                    brightness[(xcomp, ycomp)] = max(brightness[(xcomp, ycomp)] - 1, 0)
                elif cmd == "toggle":
                    brightness[(xcomp, ycomp)] += 2

    lights_on = 0
    for (xcomp, ycomp), level in brightness.items():
        lights_on += x_len_by_compressed[xcomp] * y_len_by_compressed[ycomp] * level
    return lights_on


def main():
    instructions = parse()
    on = follow(instructions)
    print(f"Part 1: {len(on)}")
    lights_on = follow_with_compression(instructions)
    print(f"Part 1 optimized: {lights_on}")
    brightness = follow_for_brightness(instructions)
    print(f"Part 2: {sum(brightness.values())}")
    lights_on = follow_for_brightness_with_compression(instructions)
    print(f"Part 2 optimized: {lights_on}")


if __name__ == "__main__":
    main()
