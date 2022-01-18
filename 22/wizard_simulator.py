from copy import deepcopy
from collections import deque
from dataclasses import dataclass
from itertools import product
from typing import List, Tuple


@dataclass(eq=True, frozen=True)
class Spell:
    name: str
    cost: int
    effect: bool
    turns: int
    heal: int
    armor: int
    damage: int
    mana: int


@dataclass
class Player:
    type: str
    hit_points: int
    damage: int
    armor: int


@dataclass
class GameState:
    player: Player
    boss: Player
    effects: List[Tuple[Spell, int]]
    mana: int
    mana_spent: int = 0

    def apply_effects(self):
        self.player.armor = 0

        updated_effects: List[Spell] = []
        for effect, remaining in self.effects:

            if effect.armor:
                if remaining > 1:
                    self.player.armor = 7

            if effect.damage:
                self.boss.hit_points -= effect.damage

            if effect.mana:
                self.mana += effect.mana

            if remaining - 1 > 0:
                updated_effects.append((effect, remaining - 1))

        self.effects = updated_effects

    def is_invalid_sequence(self, spell: Spell):
        return spell in (effect for effect, _ in self.effects)

    def cast_spell(self, spell: Spell):
        if spell.effect:
            self.effects.append((spell, spell.turns))
        else:
            self.boss.hit_points -= max(1, spell.damage - self.boss.armor)
            self.player.hit_points += spell.heal

    def boss_attack(self):
        self.player.hit_points -= max(1, self.boss.damage - self.player.armor)


MAGIC_MISSILE = Spell(
    name="Magic Missile",
    cost=53,
    effect=False,
    turns=1,
    heal=0,
    armor=0,
    damage=4,
    mana=0,
)

DRAIN = Spell(
    name="Drain",
    cost=73,
    effect=False,
    turns=1,
    heal=2,
    armor=0,
    damage=2,
    mana=0,
)

SHIELD = Spell(
    name="Shield",
    cost=113,
    effect=True,
    turns=6,
    heal=0,
    armor=7,
    damage=0,
    mana=0,
)

POISON = Spell(
    name="Poison",
    cost=173,
    effect=True,
    turns=6,
    heal=0,
    armor=0,
    damage=3,
    mana=0,
)

RECHARGE = Spell(
    name="Recharge",
    cost=229,
    effect=True,
    turns=5,
    heal=0,
    armor=0,
    damage=0,
    mana=101,
)


spells: List[Spell] = [MAGIC_MISSILE, DRAIN, SHIELD, POISON, RECHARGE]


def moves(spells: List[Spell], rounds=5):
    return sorted(product(spells, repeat=rounds), key=cost)


def cost(sequence: List[Spell]):
    return sum(spell.cost for spell in sequence)


def play(players: List[Player], sequence: List[Spell], mana, hard=False):
    queue = deque(sequence)
    state = GameState(*players, effects=[], mana=mana)

    while True:

        if not queue:
            return None

        # player turn
        if hard:
            state.player.hit_points -= 1
            if state.player.hit_points <= 0:
                return None

        spell = queue.popleft()

        if spell.cost > state.mana:
            # no more money, you loose
            return None

        state.mana -= spell.cost
        state.mana_spent += spell.cost

        state.apply_effects()
        if state.is_invalid_sequence(spell):
            return None

        if state.boss.hit_points <= 0:
            return state.mana_spent

        state.cast_spell(spell)
        if state.boss.hit_points <= 0:
            return state.mana_spent

        # boss turn
        state.apply_effects()
        if state.boss.hit_points <= 0:
            return state.mana_spent

        state.boss_attack()
        if state.player.hit_points <= 0:
            return None


def search(players: List[Player], moves: List[List[Spell]], mana=500, hard=False):
    for sequence in moves:
        mana_spent = play(deepcopy(players), list(sequence), mana, hard)
        if mana_spent:
            return mana_spent


def main():
    possible_moves = moves(spells, rounds=9)
    players = [
        Player(type="Player", hit_points=50, damage=0, armor=0),
        Player(type="Boss", hit_points=55, damage=8, armor=0),
    ]
    spent = search(players, possible_moves, mana=500)
    print(f"Part 1: {spent}")
    spent = search(players, possible_moves, mana=500, hard=True)
    print(f"Part 2: {spent}")


if __name__ == "__main__":
    main()
