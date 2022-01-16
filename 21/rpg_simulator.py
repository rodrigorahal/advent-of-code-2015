from dataclasses import dataclass
from itertools import combinations
from typing import List, Tuple


@dataclass
class Item:
    type: str
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class Player:
    type: str
    hit_points: int
    damage: int
    armor: int


WEAPONS: List[Item] = [
    Item(type="Weapons", name="Dagger", cost=8, damage=4, armor=0),
    Item(type="Weapons", name="Shortsword", cost=10, damage=5, armor=0),
    Item(type="Weapons", name="Warhammer", cost=25, damage=6, armor=0),
    Item(type="Weapons", name="Longsword", cost=40, damage=7, armor=0),
    Item(type="Weapons", name="Greataxe", cost=74, damage=8, armor=0),
]

ARMOR: List[Item] = [
    Item(type="Armor", name="Leather", cost=13, damage=0, armor=1),
    Item(type="Armor", name="Chainmail", cost=31, damage=0, armor=2),
    Item(type="Armor", name="Splintmail", cost=53, damage=0, armor=3),
    Item(type="Armor", name="Bandedmail", cost=75, damage=0, armor=4),
    Item(type="Armor", name="Platemail", cost=102, damage=0, armor=5),
]

RINGS: List[Item] = [
    Item(type="Rings", name="Damage+1", cost=25, damage=1, armor=0),
    Item(type="Rings", name="Damage+2", cost=50, damage=2, armor=0),
    Item(type="Rings", name="Damage+3", cost=100, damage=3, armor=0),
    Item(type="Rings", name="Defense+1", cost=20, damage=0, armor=1),
    Item(type="Rings", name="Defense+2", cost=40, damage=0, armor=2),
    Item(type="Rings", name="Defense+3", cost=80, damage=0, armor=3),
]


def weapons_choices():
    for weapon in WEAPONS:
        yield weapon


def armor_choices():
    yield None
    for armor in ARMOR:
        yield armor


def rings_choices():
    yield None
    for ring in RINGS:
        yield [ring]

    for pair in combinations(RINGS, 2):
        yield list(pair)


def player_possible_equips():
    equips: List[List[Item]] = []

    stack: List[Tuple[List[Item], str]] = []

    for weapon in weapons_choices():
        stack.append(([weapon], "Armor"))

    while stack:
        items, stage = stack.pop()

        if stage == "Armor":
            for armor in armor_choices():
                if armor:
                    stack.append((items + [armor], "Rings"))
                else:
                    stack.append((items, "Rings"))

        elif stage == "Rings":
            for rings in rings_choices():
                if rings:
                    stack.append((items + rings, "Ready"))
                else:
                    stack.append((items, "Ready"))

        elif stage == "Ready":
            equips.append(items)

    return sorted(equips, key=cost)


def cost(items: List[Item]):
    return sum(item.cost for item in items)


def damage(items: List[Item]):
    return sum(item.damage for item in items)


def armor(items: List[Item]):
    return sum(item.armor for item in items)


def play(players: List[Player], items: List[Item]):
    player, boss = players
    player.damage = damage(items)
    player.armor = armor(items)

    while True:
        boss.hit_points -= max(1, player.damage - boss.armor)

        if boss.hit_points <= 0:
            return player, items

        player.hit_points -= max(1, boss.damage - player.armor)

        if player.hit_points <= 0:
            return boss, items


def search(equips: List[List[Item]], highest=False, target="Player"):
    if highest:
        equips = reversed(equips)

    for items in equips:
        players = [
            Player(type="Player", hit_points=100, damage=0, armor=0),
            Player(type="Boss", hit_points=104, damage=8, armor=1),
        ]
        winner, winning_items = play(players, items)
        if winner.type == target:
            return winning_items


def main():
    equips = player_possible_equips()
    items = search(equips)
    print(f"Part 1: {cost(items)}")
    items = search(equips, highest=True, target="Boss")
    print(f"Part 2: {cost(items)}")


if __name__ == "__main__":
    main()
