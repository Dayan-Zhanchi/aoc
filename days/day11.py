import numpy as np
from itertools import combinations

"""Was thinking of solving it with naive graph algo but the computation would be infeasible. Realized that I could just 
use manhattan distance. Only tricky thing was to realize that for part2 didn't need to actually append 
1000k lists, instead just offset the original galaxy indicies"""


def parse(f, offset):
    grid = np.array([np.array(list(text)) for text in f.read().split('\n')[:-1]])
    galaxies = []
    for idx1 in np.column_stack(np.where(grid == '#')):
        x, y = idx1
        row_count = 0
        col_count = 0
        for idx2 in np.where((grid == '.').all(axis=0))[0]:
            if idx2 < y:
                col_count += 1
        for idx2 in np.where((grid == '.').all(axis=1))[0]:
            if idx2 < x:
                row_count += 1
        x += offset * row_count - row_count
        y += offset * col_count - col_count
        galaxies.append((x, y))

    return galaxies


def p1(f):
    galaxies = parse(f, 2)
    return calc_distance(galaxies)


def p2(f):
    galaxies = parse(f, 1000000)
    return calc_distance(galaxies)


def manhattan_dist(n1, n2):
    return sum([abs(s1 - s2) for s1, s2 in zip(n1, n2)])


def calc_distance(galaxies):
    pairs = list(combinations(galaxies, 2))
    dist = 0
    for n1, n2 in pairs:
        if n1 == n2:
            continue

        dist += manhattan_dist(n1, n2)

    return dist
