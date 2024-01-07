from queue import PriorityQueue
from dataclasses import dataclass

"""For some reason I couldn't get my Djikstra to work no matter what I did, so had to look this up. Creds to 
hyperneutrino: https://www.youtube.com/watch?v=2pDSooPLLkI&t=527s. It's just a straightforward Djikstra but modified to
take into account for the movement restrictions. However, this does change the visited states (higher dimensional) and that we can also revisit nodes, because
some paths might be sub-optimal in the long run due to movement restrictions."""


@dataclass
class Node:
    val: int
    pos: (int, int)


def parse(f):
    grid = [[Node(int(col), (i, j)) for j, col in enumerate(row)] for i, row in enumerate(f.read().split())]
    grid[0][0].val = 0  # we will never go back to the start
    return grid


def p1(f):
    grid = parse(f)
    return calc_lowest_heat(grid, 3, 0)


def p2(f):
    grid = parse(f)
    return calc_lowest_heat(grid, 10, 4)


def calc_lowest_heat(grid, max_step, min_step):
    q = PriorityQueue()  # ((cost, node_position, direction, steps))
    q.put((0, (0, 0), (0, 0), 0))
    visited = set()  # (node_position, direction, steps)
    target = (len(grid) - 1, len(grid[0]) - 1)
    while q:
        cost, curr_pos, direction, steps = q.get()
        if curr_pos == target and steps >= min_step:
            return cost

        state = (curr_pos, direction, steps)
        if state in visited:
            continue

        visited.add(state)
        for x, y, next_direction in get_neighbors(grid, curr_pos, direction):
            new_cost = cost + grid[x][y].val
            if steps < max_step and direction != (0, 0) and direction == next_direction:
                q.put((new_cost, (x, y), direction, steps + 1))
            if direction != next_direction and (direction == (0, 0) or steps >= min_step):
                q.put((new_cost, (x, y), next_direction, 1))


def get_neighbors(grid, pos, prev_direction):
    neighbors = []
    # could also have made them numpy lists to do vector addition, but it's a one-liner so doesn't matter
    for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        # reverse is not allowed
        if (-prev_direction[0], -prev_direction[1]) == (direction[0], direction[1]):
            continue

        coord = vector_addition(direction, pos)
        if not is_oob(grid, coord[0], coord[1]):
            neighbors.append((coord[0], coord[1], direction))

    return neighbors


def is_oob(grid, x, y):
    return False if 0 <= x < len(grid) and 0 <= y < len(grid[x]) else True


def vector_addition(direction, pos):
    return [c1 + c2 for c1, c2 in zip(direction, pos)]
