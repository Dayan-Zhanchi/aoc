from functools import cache

"""I initially implemented it without memoization. Had to get some hints on how to convert to using memoization (need 
to refresh DP and memoization). Turns out the only thing needed to do was to implement it without explicitly 
generating the arrangements, by going one character at a time and check on the group condition each time a group is 
completed. For the memoization use a cache decorator to memoize function parameters each call. credits to pred: 
https://www.reddit.com/r/adventofcode/comments/18ge41g/2023_day_12_solutions/kd0dw9e/.
My initial solution gives unique function parameters each call, since it generates all permutations of the
arrangements, this means that caching the function parameters doesn't help (they will be unique everytime).
"""


def parse(f, part):
    data = f.readlines()
    if part == 1:
        springs = [(d.split()[0] + '.', list(map(int, d.split()[1].split(',')))) for d in data]
    else:
        springs = [(((d.split()[0] + '?') * 5)[:-1] + '.', list(map(int, d.split()[1].split(','))) * 5) for d in data]

    return springs


def p1(f):
    data = parse(f, 1)
    return get_total_arrangements(data)


def p2(f):
    data = parse(f, 2)
    return get_total_arrangements(data)


def get_total_arrangements(data):
    tot = 0
    for spring, groups in data:
        tot += count_arrangements_memoization(spring, tuple(groups), 0)
        # tot += count_arrangements(spring, groups)

    return tot


def count_arrangements(springs, groups):
    if '?' not in springs:
        if is_valid(springs, groups):
            return 1
        return 0

    tot = 0
    for fill in ['#', '.']:
        tot += count_arrangements(springs.replace('?', fill, 1), groups)

    return tot


@cache
def count_arrangements_memoization(springs, groups, group_len):
    if not springs:
        if not groups and not group_len:
            return 1
        return 0

    count = 0
    if springs[0] == '?':
        count += count_arrangements_memoization('#' + springs[1:], groups, group_len) \
                 + count_arrangements_memoization('.' + springs[1:], groups, group_len)
    elif springs[0] == '#':
        count += count_arrangements_memoization(springs[1:], groups, group_len + 1)
    else:
        if group_len:
            if groups and groups[0] == group_len:
                count += count_arrangements_memoization(springs[1:], groups[1:], 0)
        else:
            count += count_arrangements_memoization(springs[1:], groups, 0)

    return count


def is_valid(arrangement, groups):
    return list(map(len, list(filter(lambda x: x != '', arrangement.split('.'))))) == groups
