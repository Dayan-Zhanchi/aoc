from dataclasses import dataclass
from itertools import groupby

"""Brute force solution would be something like O(kn^2) = O(n^2), where k = 5. Since n=1000, it should still be 
sufficient (within a few seconds at max). Hardest part for me was assigning the types to the cards in a concise way. 
Wanted to skip lots of if else conditions, so I found one pattern that was unique for all of the different types. The 
number of pairs, non pairs and the length of the most frequent letter in the current hand together formed a unique 
combination for a type. Also for part2 only needed to change the type of cards, and it sufficed to change the cards 
by replacing the most frequent letter with J (only for when determining the type and I checked that it didn't lead to 
any weird edge cases), but the for the rank calculation, the original cards were used"""


@dataclass
class Player:
    hand: str
    bid: int
    type: int  # 0-6
    rank: int


def parse(f):
    return f.readlines()


def p1(f):
    data = parse(f)
    data = [Player(line.split(' ')[0], int(line.split(' ')[1]), get_type(line.split(' ')[0], 1), 0) for line in data]
    card2val_part1 = {str(i): idx for idx, i in enumerate([*[j for j in range(2, 10)], *'TJQKA'], 2)}  # 2-14

    return calc_ranks(data, card2val_part1)


def p2(f):
    data = parse(f)
    data = [Player(line.split(' ')[0], int(line.split(' ')[1]), get_type(line.split(' ')[0], 2), 0)
            for line in data]
    card2val_part2 = {str(i): idx for idx, i in enumerate([*'J', *[j for j in range(2, 10)], *'TQKA'], 1)}  # 1-13

    return calc_ranks(data, card2val_part2)


def get_type(hand, part):
    if part == 2 and 'J' in hand:
        # ugly, but the K can be anything as long as it's not J
        letter_to_be_replaced = 'K' if hand.count('J') == 5 else max(set(hand.replace('J', '')),
                                                                     key=(hand.replace('J', '')).count)
        hand = hand.replace(letter_to_be_replaced, 'J')

    group_lens = sorted([len(i) for i in [''.join(g) for _, g in groupby(sorted(hand))]], reverse=True)
    rules = {(1, 5): 6, (2, 4): 5, (2, 3): 4, (3, 3): 3, (3, 2): 2, (4, 2): 1, (5, 1): 0}
    h_type = rules[(len(group_lens), group_lens[0])]

    return h_type


def calc_ranks(data, card2val):
    for idx1, player1 in enumerate(data):
        better_than = 1
        for idx2, player2 in enumerate(data):
            if idx1 == idx2:
                continue

            if player1.type > player2.type:
                better_than += 1
            elif player1.type == player2.type:
                better_than += check_hands(player1.hand, player2.hand, card2val)

        data[idx1].rank = better_than

    return sum([player.bid * player.rank for player in data])


def check_hands(player1, player2, card2val):
    # input does not have any duplicate hands, so no need to handle that case
    for (c1, c2) in zip(player1, player2):
        if card2val[c1] == card2val[c2]:
            continue

        if card2val[c1] > card2val[c2]:
            return 1
        else:
            return 0

    return 0
