import fileinput
from math import prod


def parse():
    boxes = [tuple(map(int, line.split("x"))) for line in fileinput.input()]
    return boxes


def paper(box):
    l, w, h = box
    return 2 * l * w + 2 * w * h + 2 * h * l + min([l * w, w * h, l * h])


def ribbon(box):
    dims = sorted(box)
    return prod(dims) + 2 * (dims[0] + dims[1])


def main():
    boxes = parse()
    print(f"Part 1: {sum(paper(box) for box in boxes)}")
    print(f"Part 2: {sum(ribbon(box) for box in boxes)}")


if __name__ == "__main__":
    main()
