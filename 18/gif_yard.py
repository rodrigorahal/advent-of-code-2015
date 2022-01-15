import fileinput


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([char for char in line.strip()])
    return grid


def animate(grid, steps=100, with_stuck=False):
    for _ in range(steps):
        grid = step(grid, with_stuck)
    return sum(state == "#" for states in grid for state in states)


def step(grid, with_stuck):
    h = len(grid)
    w = len(grid[0])

    new_grid = []
    for row, states in enumerate(grid):
        new_row = []
        for col, state in enumerate(states):
            if with_stuck and (row, col) in (
                (0, 0),
                (0, w - 1),
                (h - 1, 0),
                (h - 1, w - 1),
            ):
                new_row.append("#")
                continue

            on_neighbors = [
                grid[ra][ca]
                for ra, ca in neighbors(grid, row, col)
                if grid[ra][ca] == "#"
            ]
            if state == "#":
                if len(on_neighbors) in (2, 3):
                    new_row.append("#")
                else:
                    new_row.append(".")
            elif state == ".":
                if len(on_neighbors) == 3:
                    new_row.append("#")
                else:
                    new_row.append(".")
        new_grid.append(new_row)
    return new_grid


def neighbors(grid, row, col):
    h = len(grid)
    w = len(grid[0])

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if not (dr == dc == 0) and 0 <= (row + dr) < h and 0 <= (col + dc) < w:
                yield (row + dr), (col + dc)


def display_grid(grid):
    for states in grid:
        print(" ".join(state for state in states))
    print()


def main():
    grid = parse()
    on = animate(grid, steps=100)
    print(f"Part 1: {on}")
    on = animate(grid, steps=100, with_stuck=True)
    print(f"Part 2: {on}")


if __name__ == "__main__":
    main()
