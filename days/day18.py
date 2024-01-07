import numpy as np

"""After day 10, I just didn't want to bother with my brute-force solution, as it was tedious and slow. It also wouldn't be possible because of the enlargement in part2.
So I went with shoelace + picks today. Verified that there aren't any directions that are consecutively the same, so each instruction will result in a new vertex coordinate. 
"""

# stored as (dx, dy)
dir_to_coord = {'R': np.array([1, 0]), 'L': np.array([-1, 0]), 'U': np.array([0, 1]), 'D': np.array([0, -1])}
digit_to_dir = {'0': dir_to_coord['R'], '1': dir_to_coord['D'], '2': dir_to_coord['L'], '3': dir_to_coord['U']}
letter_to_digit = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
hex_to_b10 = lambda x: sum([int(digit) * 16 ** i if digit.isnumeric() else letter_to_digit[digit] * 16 ** i
                            for i, digit in enumerate(x[::-1])])


def parse(f):
    instructions = [(vals[0], int(vals[1]), vals[2].replace('(', '').replace(')', ''))
                    for t in f.read().split('\n')[:-1] if (vals := t.split(' '))]
    return instructions


def p1(f):
    instructions = parse(f)
    coordinates = [np.array([0, 0])]
    boundary = 0
    for direction, steps, _ in instructions:
        boundary += steps
        coordinates.append(coordinates[-1] + dir_to_coord[direction] * steps)

    area = shoelace(coordinates)
    return picks(area, boundary)


def p2(f):
    instructions = parse(f)
    coordinates = [np.array([0, 0])]
    boundary = 0
    for _, _, hex in instructions:
        steps = hex_to_b10(hex[1:6])
        direction = hex[-1]
        boundary += steps
        coordinates.append(coordinates[-1] + digit_to_dir[direction] * steps)

    area = shoelace(coordinates)
    return picks(area, boundary)


def shoelace(coords):
    # https://en.wikipedia.org/wiki/Shoelace_formula#Shoelace_formula
    area = 0
    for i in range(len(coords) - 1):
        coord1 = coords[i]
        coord2 = coords[i + 1]
        area += int(coord1[0]) * int(coord2[1]) - int(coord1[1]) * int(coord2[0])

    return np.abs(area) / 2


def picks(a, b):
    """https://en.wikipedia.org/wiki/Pick%27s_theorem
    picks theorem: A = i + b/2 - 1, where i is inner points and b is the boundary points, but we are looking for i + b, which
    is given by i + b = A + b/2 + 1 (simple rewrite by moving i to one side and adding b to both sides).
    Shoelace gives us A, and we already have b, which is the total steps
    """
    return a + b / 2 + 1
