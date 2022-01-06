import fileinput
from collections import defaultdict
from itertools import permutations
from operator import itemgetter


def parse():
    graph = defaultdict(list)
    for line in fileinput.input():
        cities, dist = line.strip().split(" = ")
        v, u = cities.split(" to ")
        graph[v].append((u, int(dist)))
        graph[u].append((v, int(dist)))
    return graph


def search(graph):
    valid = []
    for source, target in permutations(graph, 2):
        for path, dist in paths(graph, source, target):
            if len(path) == len(graph):
                valid.append((path, dist))
    return valid


def paths(graph, source, target):
    stack = [(source, [source], 0, {source})]
    paths = []

    while stack:
        city, path, path_len, seen = stack.pop()

        if city == target:
            paths.append((path, path_len))

        for next, dist in graph[city]:
            if next in seen:
                continue
            stack.append((next, path + [next], path_len + dist, {*seen, next}))

    return paths


def main():
    graph = parse()
    paths = search(graph)
    print(f"Part 1: {min(paths, key=itemgetter(1))}")
    print(f"Part 2: {max(paths, key=itemgetter(1))}")


if __name__ == "__main__":
    main()
