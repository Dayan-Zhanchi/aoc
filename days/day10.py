import math
from copy import deepcopy

"""Naive, slow and tedious approach: padded the maze so I could then mark the nodes that were outside (padding 
allows possible paths going outside the maze to connect with the outside nodes). Checking for nodes not in the loop, 
not being the padded characters and not being outside to find the inside nodes. In hindsight saw that there were some 
geometry algs that could have made the solution significantly shorter, especially the scanline and the even/odd 
parity approach or picks + shoelace. One thing to note, I add space and M in entries as an ugly way to handle the case 
of identifying nodes that are in the loop."""


def parse(f):
    return [list(text) for text in f.read().split('\n')[:-1]]


def p1(f):
    grid = parse(f)
    grid = mark_main_loop(grid)
    counter = sum([1 if 'M' in g2 else 0 for x, g1 in enumerate(grid) for g2 in g1])

    return math.ceil(counter / 2)


# very slow, approx 1 minute
def p2(f):
    grid = parse(f)
    grid = mark_main_loop(grid)
    padded_grid = pad_grid(grid)
    outsides = mark_outside_loop(padded_grid)
    count = 0
    for x, row in enumerate(padded_grid):
        for y, col in enumerate(row):
            if (x, y) not in outsides and 'M' not in col and '#' not in col:
                count += 1

    return count


def mark_main_loop(grid):
    s_x, s_y = [(x, y) for x, l in enumerate(grid) for y, e in enumerate(l) if e == 'S'][0]
    for x, y in get_nswe(s_x, s_y):
        prev_coord = s_x, s_y
        val = grid[x][y]
        if not is_oob(grid, x, y) and val != '.' and prev_coord in get_connection_map(x, y)[val]:
            curr_val = val
            starting_coord = (x, y)
        else:
            continue

        while curr_val != 'S' and not is_oob(grid, x, y):
            x_next, y_next = get_next_node_coord(prev_coord, (x, y), curr_val)
            grid[x][y] = (grid[x][y] + ' ' + 'M')
            prev_coord = x, y
            x, y = x_next, y_next
            curr_val = grid[x][y]

        if curr_val == 'S':
            # assign the correct pipe to S
            pipe = [key for key, item in get_connection_map(x, y).items()
                    if starting_coord in item and prev_coord in item][0]
            grid[x][y] = pipe + ' ' + 'M'
            break

    return grid


def pad_grid(grid):
    padded_grid = deepcopy(grid)
    for x in range(len(grid)):
        # vertical padding
        if x < len(grid) - 1:
            padded_grid.insert(2 * x + 1, list('#' * len(grid[x])))
            for y in range(len(grid[x])):
                if is_connected(grid, (x, y), (x + 1, y)):
                    padded_grid[2 * x + 1][y] = '| M'

        # horizontal padding
        for y in range(len(grid[x]) - 1):
            padding_h = '#'
            if is_connected(grid, (x, y), (x, y + 1)):
                padding_h = '- M'

            padded_grid[2 * x].insert(2 * y + 1, padding_h)
            # second vertical padding
            if x < len(grid) - 1:
                padded_grid[2 * x + 1].insert(2 * y + 1, '#')

    # add border around to ensure starting outside the loop
    padded_grid.append(list('#' * len(padded_grid[0])))
    padded_grid.insert(0, list('#' * len(padded_grid[0])))
    [padded_grid[x].append('#') for x in range(len(padded_grid))]
    [padded_grid[x].insert(0, '#') for x in range(len(padded_grid))]

    return padded_grid


def mark_outside_loop(grid):
    # BFS
    q = [(0, 0)]
    visited = []
    while q:
        x, y = q.pop(0)
        if not is_oob(grid, x, y) and (x, y) not in visited and 'M' not in grid[x][y]:
            visited.append((x, y))
            for d in get_nswe(x, y):
                q.append(d)

    return visited


def get_next_node_coord(prev_coord, current_coord, val):
    x, y = current_coord
    next_node = get_connection_map(x, y)
    next_node[val].remove(prev_coord)

    return next_node[val][0]


def get_nswe(x, y):
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def get_connection_map(x, y):
    n, s, w, e = get_nswe(x, y)
    next_node = {'|': [n, s], '-': [e, w], 'L': [n, e], 'J': [n, w], '7': [s, w],
                 'F': [s, e]}
    return next_node


def is_connected(grid, e1, e2):
    x_e1, y_e1 = e1[0], e1[1]
    x_e2, y_e2 = e2[0], e2[1]
    e1_val = grid[x_e1][y_e1].split()
    e2_val = grid[x_e2][y_e2].split()
    if len(e1_val) > 1 and len(e2_val) > 1:
        e1_connections = get_connection_map(x_e1, y_e1)[e1_val[0]]
        e2_connections = get_connection_map(x_e2, y_e2)[e2_val[0]]
        return e1 in e2_connections and e2 in e1_connections

    return False


def is_oob(grid, x, y):
    return False if 0 <= x < len(grid) and 0 <= y < len(grid[x]) else True


def print_grid(grid):
    for x, p in enumerate(grid):
        for y, q in enumerate(grid[x]):
            if 'M' in q:
                q = q.split()[0]
            print(q, end='')
        print()
