import numpy as np
from copy import deepcopy

"""Pure imperative this time, not functional style at all as I couldn't think of smart tricks to do it. I used numpy 
for ease of extraction of columns. This was basic traversing, I think similar to flood fill, but the directions we go 
are only determined by the mirrors we encounter. One could probably memoize the energy that each paths contribute 
with, but brute force still works within a few seconds. Also horrible code, due to axis flags this results in 
infestation of conditionals for index assignments, although only one liners luckily with inline conditional. 
Grid_for_marking is only for debugging purposes"""


def parse(f):
    return np.array([np.array(list(t)) for t in f.read().split()])


def p1(f):
    grid = parse(f)
    energy, _ = traverse_grid(grid, ('E', (0, 0)))
    return energy


def p2(f):
    grid = parse(f)
    starting_point_candidates = []
    # format (direction, coordinate)
    for direction in ['N', 'S', 'W', 'E']:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if 0 < x < len(grid) - 1:
                    if 0 < y < len(grid[x]) - 1:
                        continue
                if (s := (direction, (x, y))) not in starting_point_candidates:
                    starting_point_candidates.append(s)

    energy = -1
    best_marked = None
    for s in starting_point_candidates:
        e, marked = traverse_grid(grid, s)
        if e > energy:
            energy = e
            best_marked = marked

    # print(best_marked)

    return energy


def traverse_grid(grid, starting_point):
    grid_for_marking = deepcopy(grid)
    q = [starting_point]  # (direction, (x, y))
    is_start = True
    # a visited path means we will fill the exact same tiles again if we follow the path, and it's uniquely
    # identified as the direction and the coordinate. However, for some reason I decided to only save the coords at
    # the mirror, which still works, but need to reach the mirror before can make a decision,
    # this made the code unnecessarily bloated because each iteration I kind of jump to the upcoming mirror, but could have instead just saved all tiles leading up to the upcoming mirror
    visited = {}  # (direction, mirror)
    energized = {}  # (x, y)
    energy = 0
    steps = {'N': (0, -1), 'S': (0, 1), 'E': (1, 1), 'W': (1, -1)}  # (axis, step)
    while q:
        direction, (x, y) = q.pop(0)
        if (direction, (x, y)) in visited:
            continue

        axis, step = steps[direction]
        grid_chunk, curr_idx1 = (grid[x], y) if axis else (grid[:, y], x)
        # if step is negative then we are going backwards otherwise forward, so have to adjust the start and stop in
        # range loop for that purpose
        start, stop = (curr_idx1, len(grid_chunk)) if step > 0 else (curr_idx1, -1)
        if is_oob(grid_chunk, start):
            continue

        # find the next mirror
        mirror = None
        for i in range(start, stop, step):
            energy_idx = (x, i) if axis else (i, y)
            if energy_idx not in energized:
                energy += 1
                energized[energy_idx] = True
                grid_for_marking[energy_idx] = '#'

            if grid_chunk[i] != '.' and (is_start or i != start):
                mirror, mirror_idx = grid_chunk[i], (x, i) if axis else (i, y)
                break

        if mirror:
            new_direction = get_direction(mirror, direction)
            if isinstance(new_direction, tuple):
                q.append((new_direction[0], mirror_idx))
                q.append((new_direction[1], mirror_idx))
            else:
                q.append((new_direction, mirror_idx))

        visited[(direction, (x, y))] = True
        is_start = False

    return energy, grid_for_marking


def get_direction(mirror, direction):
    if mirror == '|' and (direction == 'E' or direction == 'W'): return 'S', 'N'
    if mirror == '|' and direction == 'N': return 'N'
    if mirror == '|' and direction == 'S': return 'S'

    if mirror == '-' and (direction == 'N' or direction == 'S'): return 'E', 'W'
    if mirror == '-' and direction == 'E': return 'E'
    if mirror == '-' and direction == 'W': return 'W'

    if mirror == '\\' and direction == 'N': return 'W'
    if mirror == '\\' and direction == 'S': return 'E'
    if mirror == '\\' and direction == 'E': return 'S'
    if mirror == '\\' and direction == 'W': return 'N'

    if mirror == '/' and direction == 'N': return 'E'
    if mirror == '/' and direction == 'S': return 'W'
    if mirror == '/' and direction == 'E': return 'N'
    if mirror == '/' and direction == 'W': return 'S'


def is_oob(grid, x):
    return not (0 <= x < len(grid))
