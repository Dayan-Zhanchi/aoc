"""Zip helped alot here. Iterated through all possible reflection lines and
for each candidate line used zip to pair the rows and cols respectively. The only tricky thing was getting the
indices correct for zip to work. For part2 a key insight that made it easy was that only needed to find exactly in
total 1 character difference between all pair to find the desired reflection line. A cool trick to check the 1
difference is to sum over all booleans, since False gives 0 while True gives 1, so there should only ever be 1 True
value for the reflection line that is the desired one"""


def parse(f):
    return list(map(str.split, f.read().split('\n\n')))


def p1(f):
    grids = parse(f)
    return calc_total_sum(grids, 1)


def p2(f):
    grids = parse(f)
    return calc_total_sum(grids, 2)


def calc_total_sum(grids, part):
    total = 0
    for g in grids:
        total += calc_reflection_number(g, 0, part) + calc_reflection_number(list(zip(*g)), 1, part)
    return total


def calc_reflection_number(grid, axis, part):
    for reflection_line_idx in range(len(grid)):
        if reflection_line_idx == 0:
            # zero index always gives empty list, but this gives true in all() so need to skip this case
            continue

        if part == 1:
            if all(m1 == m2 for m1, m2 in zip(grid[:reflection_line_idx][::-1], grid[reflection_line_idx:])):
                return ref_number_sum(reflection_line_idx, axis)
        else:
            if sum(l1 != l2 for m1, m2 in zip(grid[:reflection_line_idx][::-1], grid[reflection_line_idx:])
                   for l1, l2 in zip(m1, m2)) == 1:
                return ref_number_sum(reflection_line_idx, axis)

    return 0


def ref_number_sum(reflection_number, axis):
    return 100 * reflection_number if axis == 0 else reflection_number
