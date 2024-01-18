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
    q = [(0, 1, 0, set(), 0, 1)]  # x, y, path length, visited, junction_x, junction_y
    max_iter = 3 * 10 ** 5
    iter = 0
    while q and iter < max_iter:
        x, y, path_len, visited, jx, jy = q.pop(0)
        if (x, y) in visited:
            continue

        visited.add((x, y))
        neighbors = get_neighbors(grid, x, y, 2)
        if len(neighbors) > 2:
            # non-directional graph
            edges[(jx, jy)].add((x, y, path_len))
            edges[(x, y)].add((jx, jy, path_len))
            jx, jy = x, y  # new junction point
            path_len = 0  # reset path length for next junction
            visited = deepcopy(visited)
        for cx, cy, _ in neighbors:
            if (cx, cy) not in visited:
                q.append((cx, cy, path_len + 1, visited, jx, jy))
        iter += 1

    # another BFS to find the length between the end and the closest junction to it
    q = [(r, c)]
    visited = set()
    path_len = 0
    jx, jy = 0, 0
    while q:
        x, y = q.pop(0)
        if (x, y) in visited:
            continue

        visited.add((x, y))
        neighbors = get_neighbors(grid, x, y, 2)
        if len(neighbors) > 2:
            # found it
            jx = x
            jy = y
            break
        for cx, cy, _ in neighbors:
            if (cx, cy) not in visited:
                path_len += 1
                q.append((cx, cy))
    return grid, edges, r, c, (jx, jy, path_len)


def p1(f):
    grid, r, c = parse(f, 1)
    return dfs(grid, r, c, 0, 1, set(), 0, 1)


# slow 50s
def p2(f):
    grid, edges, r, c, jx, jy, path_len = parse(f, 2)
    edges[(r, c)].add((jx, jy, path_len))
    edges[(jx, jy)].add((r, c, path_len))
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
