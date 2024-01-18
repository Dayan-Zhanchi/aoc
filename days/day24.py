from itertools import combinations
import numpy as np
import sympy


def parse(f, part):
    a, b = [], []
    for data in f.read().splitlines():
        res_vector, coefficient_vector = [[number for number in v.split(',')] for v in data.replace(' ', '').split('@')]
        res_vector = list(map(int, res_vector))
        coefficient_vector = list(map(int, coefficient_vector))
        # moving to other side, need to isolate the constant for part 1
        coefficient_vector = [c * -1 for c in coefficient_vector] if part == 1 else coefficient_vector
        a.append(np.array(coefficient_vector))
        b.append(np.array(res_vector))
    return list(zip(a, b))


def p1(f):
    data = parse(f, 1)
    pairs = combinations(data, 2)
    lower, upper = 200000000000000, 400000000000000
    # lower, upper = 7, 27  # for sample
    intersections = 0
    for pair1, pair2 in pairs:
        # coefficient matrix with x,y,a,b each row
        coefficient_matrix_a_pair1 = [[1, 0, pair1[0][0], 0], [0, 1, pair1[0][1], 0]]
        coefficient_matrix_a_pair2 = [[1, 0, 0, pair2[0][0]], [0, 1, 0, pair2[0][1]]]
        a = np.concatenate((coefficient_matrix_a_pair1, coefficient_matrix_a_pair2), axis=0)
        b = np.concatenate((pair1[1][0:2], pair2[1][0:2]), axis=0)
        try:
            x, y, s, t = np.linalg.solve(a, b)
            if lower <= x <= upper and lower <= y <= upper and s >= 0 and t >= 0:
                intersections += 1
        except np.linalg.LinAlgError as _:
            continue

    return intersections


def p2(f):
    data = parse(f, 2)
    xs, ys, zs, vxs, vys, vzs = sympy.symbols('xs, ys, zs, vxs, vys, vzs')
    equations = []
    for idx, d in enumerate(data[:3]):
        vxr, vyr, vzr = d[0]
        xr, yr, zr = d[1]
        t = sympy.symbols(f"t{idx}")
        equations.append(xr + vxr * t - xs - vxs * t)
        equations.append(yr + vyr * t - ys - vys * t)
        equations.append(zr + vzr * t - zs - vzs * t)
    res = sympy.solve(equations)[0]
    return res[xs] + res[ys] + res[zs]
