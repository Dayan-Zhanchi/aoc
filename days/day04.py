import re

"""
in hindsight could have used AND operation between two sets (with Set() function) of winning numbers and scratch
numbers to get count
"""


def parse(f):
    return f.readlines()


def p1(f):
    data = parse(f)
    points = 0
    for d in data:
        count = count_matching_numbers(d)
        points += 2 ** (count - 1) if count > 0 else 0

    return points


def p2(f):
    data = parse(f)
    card_occurences = [1] * len(data)
    for idx, d in enumerate(data):
        count = count_matching_numbers(d)
        if count > 0:
            for i in range(idx + 1, idx + count + 1):
                if i >= len(card_occurences):
                    break
                card_occurences[i] += card_occurences[idx]

    return sum(card_occurences)


def count_matching_numbers(d):
    p = r'\d+'
    numbers = d.split(':')[1].split('|')
    winning_numbers = re.findall(p, numbers[0])
    scratch_cards = re.findall(p, numbers[1])
    count = 0
    for s in scratch_cards:
        if s in winning_numbers:
            count += 1

    return count
