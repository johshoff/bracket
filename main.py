#!/usr/bin/env python3

# need annotation for circular dependency Player/Match to work
from __future__ import annotations

import zlib
from dataclasses import dataclass
from itertools import zip_longest
from collections import defaultdict

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
    Bracket([Player() for _ in range(16)], [], 'black'),

    # losers brackets
    Bracket([], [], 'red'),
    Bracket([], [], 'yellow'),
]
group_brackets = True

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

# combine brackets by having winners from two brackets play a match in the "upper" bracket
while True:
    pending_brackets = [b for b in brackets if len(b.pending_players) > 0]
    if len(pending_brackets) <= 1:
        # there should be one player left: the winner
        assert(len(pending_brackets) == 1)
        break

    low_bracket = pending_brackets[-1]
    top_bracket = pending_brackets[-2]
    a = low_bracket.pending_players.pop()
    b = top_bracket.pending_players.pop()
    m = add_match(a, b, top_bracket)
    top_bracket.pending_players.append(Player(m))

def print_dot_graph(matches):
    print('digraph {')
    if group_brackets:
        bracket_graphs = defaultdict(list)
        for m in matches:
            bracket_graphs[id(m.bracket)].append(m)
        for bracket_id, bracket_matches in bracket_graphs.items():
            # the name "cluster" is significant
            print('  subgraph cluster_%s {' % bracket_id)
            print('    color=none')
            for m in bracket_matches:
                print('    %s [color=%s,label=""]' % (id(m), m.bracket.color))
            print('  }')
    for m in matches:
        if not group_brackets:
            print('  %s [color=%s,label=""]' % (id(m), m.bracket.color))
        for player in [m.a, m.b]:
            if player.last_match is not None:
                color = 'black' if player.is_winner else 'red'
                print('  %s -> %s [color=%s,label=""]' % (id(player.last_match), id(m), color))
    print('}')

print_dot_graph(matches)
