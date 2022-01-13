import fileinput
from itertools import product
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse() -> List[Ingredient]:
    ingredients = []
    for line in fileinput.input():
        words = line.strip().split(" ")
        name = words[0].strip(":")
        capacity = int(words[2].strip(","))
        durability = int(words[4].strip(","))
        flavor = int(words[6].strip(","))
        texture = int(words[8].strip(","))
        calories = int(words[10])
        ingredients.append(
            Ingredient(name, capacity, durability, flavor, texture, calories)
        )
    return ingredients


def teaspoons(ingredients: List[Ingredient], target: int = 100):
    return [
        measures
        for measures in product(range(target + 1), repeat=len(ingredients))
        if sum(measures) == target
    ]


def search(
    ingredients: List[Ingredient],
    measures: Tuple[int],
    calories_target: Optional[int] = None,
):
    scores = [
        scr
        for scr, calories in [score(ingredients, measure) for measure in measures]
        if calories_target is None or calories == calories_target
    ]
    return max(scores)


def score(ingredients: List[Ingredient], spoons: Tuple[int]):
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    calories = 0
    for ingredient, qty in zip(ingredients, spoons):
        capacity += ingredient.capacity * qty
        durability += ingredient.durability * qty
        flavor += ingredient.flavor * qty
        texture += ingredient.texture * qty
        calories += ingredient.calories * qty
    return (
        max(0, capacity) * max(0, durability) * max(0, flavor) * max(0, texture)
    ), calories


def main():
    ingredients = parse()
    measures = teaspoons(ingredients)
    print(f"Part 1: {search(ingredients, measures)}")
    print(f"Part 2: {search(ingredients, measures, calories_target=500)}")


if __name__ == "__main__":
    main()
