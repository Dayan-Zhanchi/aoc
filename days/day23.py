import numpy as np
from collections import defaultdict
import sys
from copy import deepcopy

sys.setrecursionlimit(10 ** 7)


def parse(f, part):
    grid = [data for data in f.read().splitlines()]
    r, c = len(grid) - 1, len(grid[-1]) - 2
    if part == 1:
        return grid, r, c
    return compress_graph(grid, r, c)


def compress_graph(grid, r, c):
    # BFS only keep start, end and junctions
    edges = defaultdict(lambda: set())  # adjacency list
    junctions = {(x, y) for x, row in enumerate(grid) for y, _ in enumerate(row)
                 if len(get_neighbors(grid, x, y, 2)) > 2}
    junctions.add((0, 1))
    junctions.add((r, c))
    for j in junctions:
        jx, jy = j
        q = [(cx, cy, 1) for (cx, cy, _) in get_neighbors(grid, jx, jy, 2)]
        visited = {(jx, jy)}
        while q:
            x, y, path_len = q.pop(0)
            if (x, y) in visited:
                continue

            visited.add((x, y))
            neighbors = get_neighbors(grid, x, y, 2)
            if len(neighbors) > 2:
                edges[(jx, jy)].add((x, y, path_len))
                edges[(x, y)].add((jx, jy, path_len))
            else:
                for cx, cy, _ in neighbors:
                    if (cx, cy) not in visited:
                        q.append((cx, cy, path_len + 1))
    return grid, edges, r, c


def p1(f):
    grid, r, c = parse(f, 1)
    return dfs(grid, r, c, 0, 1, set(), 0, 1)


# slow 30s
def p2(f):
    grid, edges, r, c = parse(f, 2)
    return dfs(edges, r, c, 0, 1, set(), 0, 2)


def dfs(graph, r, c, x, y, visited, curr_path_len, part):
    if (x, y) == (r, c):
        return curr_path_len

    candidates = 0
    neighbors = get_neighbors(graph, x, y, 1) if part == 1 else graph[(x, y)]
    for cx, cy, cost in neighbors:
        if (cx, cy) not in visited:
            visited.add((cx, cy))
            candidates = max(dfs(graph, r, c, cx, cy, visited, curr_path_len + cost, part), candidates)
            visited.remove((cx, cy))
    return candidates


def get_neighbors(grid, x, y, part):
    neighbors = []
    if part == 1:
        neighbor_dxdy = {'^': [np.array([-1, 0])], '>': [np.array([0, 1])], 'v': [np.array([1, 0])],
                         '<': [np.array([0, -1])],
                         '.': [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]}
        neighbor_dxdy = neighbor_dxdy[grid[x][y]]
    else:
        neighbor_dxdy = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])] \
            if grid[x][y] in 'v^<>.' else []

    for dxdy in neighbor_dxdy:
        new_x, new_y = np.array([x, y]) + dxdy
        if not is_oob(grid, new_x, new_y) and grid[new_x][new_y] != '#':
            neighbors.append((new_x, new_y, 1))
    return neighbors


def is_oob(grid, x, y):
    return False if 0 <= x < len(grid) and 0 <= y < len(grid[x]) else True
