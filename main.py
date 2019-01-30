#!/usr/bin/env python3

# need annotation for circular dependency Player/Match to work
from __future__ import annotations

import zlib
from dataclasses import dataclass
from itertools import zip_longest

@dataclass
class Bracket:
    pending_players: list
    pending_matches: list
    color: str

@dataclass
class Player:
    last_match: Match = None
    is_winner: bool = True

@dataclass
class Match:
    a: Player
    b: Player
    bracket: Bracket

brackets = [
    # normal bracket
    Bracket([Player() for _ in range(32)], [], 'black'),

    # losers bracket
    Bracket([], [], 'red'),
]

matches = []

def add_match(a, b, bracket):
    m = Match(a, b, bracket)
    matches.append(m)
    return m

while any(len(b.pending_players) > 1 for b in brackets):
    for bracket, next_bracket in zip_longest(brackets, brackets[1:]):
        while len(bracket.pending_players) > 1:
            a = bracket.pending_players.pop()
            b = bracket.pending_players.pop()
            m = add_match(a, b, bracket)
            bracket.pending_matches.append(m)

        while len(bracket.pending_matches) > 0:
            m = bracket.pending_matches.pop()
            winner = Player(m)
            loser  = Player(m, False)
            bracket.pending_players.append(winner)

            if next_bracket is not None:
                next_bracket.pending_players.append(loser)

# hardcoded for two brackets, but could be generalized
a = brackets[0].pending_players.pop()
b = brackets[1].pending_players.pop()
add_match(a, b, brackets[0])

def print_dot_graph(matches):
    print('digraph {')
    for m in matches:
        print('  %s [color=%s,label=""]' % (id(m), m.bracket.color))
        for player in [m.a, m.b]:
            if player.last_match is not None:
                color = 'black' if player.is_winner else 'red'
                print('  %s -> %s [color=%s,label=""]' % (id(player.last_match), id(m), color))
    print('}')

print_dot_graph(matches)
