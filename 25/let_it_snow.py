def generate(row, column, seed):
    prev = seed
    for start_row in range(2, row + column):
        r = start_row
        for c in range(1, start_row + 1):
            curr = (prev * 252533) % 33554393
            if r == row and c == column:
                return curr
            r -= 1
            prev = curr


def main():
    ROW, COLUMN = 3010, 3019
    SEED = 20151125
    code = generate(ROW, COLUMN, SEED)
    print(f"Part 1: {code}")


if __name__ == "__main__":
    main()
