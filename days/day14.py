"""credits to i_have_no_biscuits: https://www.reddit.com/r/adventofcode/comments/18i0xtn/2023_day_14_solutions
/kdbwi4k/ for showing a nice one-liner for sliding the rocks. Wanted to do this more functional style, so I had a
groupby approach: [''.join(list(group)) for key, group in groupby(input_string, key=lambda x: '.' in x or 'O' in x)]
, but didn't think about split at all. Reason why need to tuple the lists is to be able to hash the grid in a dictionary as
key (lists arent hashable). One thing to note for the cycle detection is that the there's a rampup before entering the main cycle,
thus explaining the extra subtractions being made on the mod"""


def parse(f):
    # only need to transpose once to make cols into rows
    return transpose([t for t in f.read().split()])


def p1(f):
    grid = parse(f)
    return calc_sum(slide(grid))


def p2(f):
    grid = parse(f)
    layouts = {}
    total_cycles = 1000000000
    for i in range(1, total_cycles + 1):
        grid = cycle(grid)
        if grid in layouts:
            cycle_number = i
            break

        layouts[grid] = i

    true_cycle_length = cycle_number - layouts[grid]
    remaining_total_cycles = total_cycles - cycle_number
    offset = remaining_total_cycles % true_cycle_length

    for _ in range(offset):
        grid = cycle(grid)

    return calc_sum(grid)


def calc_sum(grid):
    tot = 0
    for row in grid:
        for idx, tile in enumerate(row[::-1], 1):
            tot += idx * (tile == 'O')
    return tot


def cycle(grid):
    for _ in range(4):
        grid = rotate_90_counter_clockwise(slide(grid))
    return grid


def slide(grid):
    return tuple([
        '#'.join('O' * s.count('O') + '.' * s.count('.') for s in row.split('#')) for row in grid])


def rotate_90_counter_clockwise(grid):
    return tuple(list(map("".join, zip(*grid)))[::-1])


def transpose(grid):
    return tuple([''.join(list(x)) for x in zip(*grid)])
