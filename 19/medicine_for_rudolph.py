import fileinput
from collections import defaultdict, deque
from random import shuffle


def parse():
    replacements_by_element = defaultdict(list)
    rules = []

    last = False
    for line in fileinput.input():
        if line == "\n":
            last = True

        if last:
            molecule = line.strip()

        else:
            element, compound = line.strip().split(" => ")
            replacements_by_element[element].append(compound)
            rules.append((element, compound))

    return replacements_by_element, molecule, rules


def one_replacements(molecule, replacements_by_element):
    molecules = set()

    i = 0
    while i < len(molecule) - 1:
        curr, nxt = molecule[i], molecule[i + 1]
        if curr.isupper() and nxt.isupper():
            molecules.update(
                apply_replacements(
                    molecule, replacements_by_element, curr, i, double=False
                )
            )
            i += 1
        elif curr.isupper() and nxt.islower():
            molecules.update(
                apply_replacements(
                    molecule, replacements_by_element, curr + nxt, i, double=True
                )
            )
            i += 2

    last = molecule[-1]
    if last.isupper() or last == "e":
        molecules.update(
            apply_replacements(
                molecule, replacements_by_element, last, len(molecule) - 1, double=False
            )
        )

    return molecules


def apply_replacements(molecule, replacements_by_element, element, idx, double=False):
    if element not in replacements_by_element:
        return []
    diff = 2 if double else 1
    return [
        molecule[:idx] + replacement + molecule[idx + diff :]
        for replacement in replacements_by_element[element]
    ]


def search(molecule, replacements):
    queue = deque([("e", 0)])
    seen = set()

    while queue:
        curr, steps = queue.popleft()

        if curr in seen:
            continue

        seen.add(curr)

        if curr == molecule:
            return steps

        for new_molecule in one_replacements(curr, replacements):
            if new_molecule not in seen and not new_molecule.startswith("CR"):
                queue.append((new_molecule, steps + 1))


def random_search(molecule, rules):
    steps = 0

    curr = molecule
    while curr != "e":
        changed = False
        for element, compound in rules:
            if compound in curr:
                curr = curr.replace(compound, element, 1)
                steps += 1
                changed = True
                break

        if not changed:
            steps = 0
            curr = molecule
            shuffle(rules)
    return steps


def main():
    replacements_by_element, molecule, rules = parse()
    molecules = one_replacements(molecule, replacements_by_element)
    print(f"Part 1: {len(molecules)}")

    steps = random_search(molecule, rules)
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
