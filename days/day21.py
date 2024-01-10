import numpy as np
import math
from scipy.interpolate import lagrange

"""
For this day I had already spoilt it for myself by looking at the memes, so I knew what to do, although I still don't
understand the details as to why it works, perhaps this explanation shines some light: https://www.reddit.com/r/adventofcode/comments/18ofc8i/2023_day_21_part_2_intuition_behind_solution/
"""


def parse(f):
    return [g for g in f.read().splitlines()]


def p1(f):
    grid = parse(f)
    start = [(i, j) for i, row in enumerate(grid) for j, col in enumerate(row) if col == 'S'][0]
    return get_number_of_plots(grid, 64, start)


# slow approx 2m40s
def p2(f):
    grid = parse(f)
    # enlarge the grid by factor * factor, just big enough for the steps
    factor = 59  # has to be odd in order to have a middle S
    grid = [factor * row for _ in range(factor) for row in grid]
    # find start in the middle in a square
    middle_idx = math.ceil(factor / 2) - 1
    s_pos = [(i, j) for i, row in enumerate(grid) for j, col in enumerate(row) if col == 'S']
    start = s_pos[factor * middle_idx + middle_idx]

    original_steps = 26501365
    steps = [65, 65 + 131, 65 + 131 * 2]
    possibilities = []
    for s in steps:
        possibilities.append(get_number_of_plots(grid, s, start))

    print(possibilities)  # 3691, 32975, 91439
    # 26501365 = 202300 * 131 + 65
    poly = lagrange([0, 1, 2], possibilities)
    poly = np.polynomial.polynomial.Polynomial(poly.coef[::-1])

    return poly((original_steps - 65) / 131)


def get_number_of_plots(grid, steps, start):
    possibilities = set(start)
    for _ in range(steps):
        candidates = set()
        for curr_pos in possibilities:
            for pos in [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]:
                x, y = np.array(curr_pos) + pos
                if not is_oob(grid, x, y):
                    if grid[x][y] != '#':
                        candidates.add((x, y))
        possibilities = candidates

    return len(possibilities)


def is_oob(grid, x, y):
    return False if 0 <= x < len(grid) and 0 <= y < len(grid[x]) else True


def print_grid(grid):
    for row in grid:
        print(row)
