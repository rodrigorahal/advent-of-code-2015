from dis import dis
import fileinput

TICKER_TAPE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse():
    sues = {}
    for line in fileinput.input():
        sue = {}
        words = line.strip().split(" ")
        idx = int(words[1].strip(":"))
        for i in range(len(words) - 1):
            if i < 2 or i % 2:
                continue
            compound = words[i].strip(":")
            amount = int(words[i + 1].strip(","))
            sue[compound] = amount
        sues[idx] = sue
    return sues


def discard(sues, with_ranges=False):
    discarded = set()
    for idx, sue in sues.items():
        for compound, amount in sue.items():
            if with_ranges and compound in ("cats", "trees"):
                if TICKER_TAPE[compound] >= amount:
                    discarded.add(idx)
            elif with_ranges and compound in ("pomeranians", "goldfish"):
                if TICKER_TAPE[compound] <= amount:
                    discarded.add(idx)
            else:
                if TICKER_TAPE[compound] != amount:
                    discarded.add(idx)
    return {idx: sue for idx, sue in sues.items() if idx not in discarded}


def main():
    sues = parse()
    print(f"Part 1: {discard(sues)}")
    print(f"Part 2: {discard(sues, with_ranges=True)}")


if __name__ == "__main__":
    main()
