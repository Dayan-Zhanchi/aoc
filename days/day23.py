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
    q = [(0, 1, 0, set(), 0, 1)]
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
        for cx, cy in neighbors:
            if (cx, cy) not in visited:
                q.append((cx, cy, path_len + 1, visited, jx, jy))
        iter += 1
        # print(f"{iter}: {len(q)}")
    return grid, edges, r, c


def p1(f):
    grid, r, c = parse(f, 1)
    return dfs1(grid, 0, 1, set(), 0)


# slow 50s
def p2(f):
    grid, edges, r, c = parse(f, 2)
    print(len(edges))
    print(edges)
    edges[(r, c)].add((129, 125, 121))
    edges[(129, 125)].add((r, c, 121))
    return dfs2(edges, grid, 0, 1, set(), 0)


def dfs1(grid, x, y, visited, curr_path_len):
    if (x, y) == (len(grid) - 1, len(grid[-1]) - 2):
        return curr_path_len

    candidates = 0
    for cx, cy in get_neighbors(grid, x, y, 1):
        if (cx, cy) not in visited:
            visited.add((cx, cy))
            candidates = max(dfs1(grid, cx, cy, visited, curr_path_len + 1), candidates)
            visited.remove((cx, cy))
    return candidates


def dfs2(graph, grid, x, y, visited, curr_path_len):
    if (x, y) == (len(grid) - 1, len(grid[-1]) - 2):
        return curr_path_len

    candidates = 0
    for cx, cy, cost in graph[(x, y)]:
        if (cx, cy) not in visited:
            visited.add((cx, cy))
            candidates = max(dfs2(graph, grid, cx, cy, visited, curr_path_len + cost), candidates)
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
        neighbor_dxdy = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])] if grid[x][
                                                                                                          y] in 'v^<>.' else []

    for dxdy in neighbor_dxdy:
        new_x, new_y = np.array([x, y]) + dxdy
        if not is_oob(grid, new_x, new_y) and grid[new_x][new_y] != '#':
            neighbors.append((new_x, new_y))
    return neighbors


def is_oob(grid, x, y):
    return False if 0 <= x < len(grid) and 0 <= y < len(grid[x]) else True
