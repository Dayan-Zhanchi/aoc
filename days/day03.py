"""
1. look around each symbol and find the numbers that way.
2. another way is to consider each direction for each number, doesn't really matter though, will be O(k*N)=O(N)
regardless, where N is input length, go with whichever is easier to code.

In hindsight method 1 works for both part1 and 2, but method 2 needs to be modified to work with p2. I used method 2.
The modification I did was to store position of the symbol in dictionary as key and the value as the numbers adjacent
to the symbol."""


def parse(f):
    return f.readlines()


def p1(f):
    data = parse(f)
    numbers, _ = get_gear_and_numbers(data)
    return sum(numbers)


def p2(f):
    data = parse(f)
    from math import prod
    _, gears = get_gear_and_numbers(data)
    return sum([prod(numbers) for pos, numbers in gears.items() if len(numbers) == 2])


def get_gear_and_numbers(grid):
    # from left to right, top to bottom
    numbers = []
    gear_adjacents = {}
    for x, i in enumerate(grid):
        number = ''
        pos = None
        for y, j in enumerate(grid[x]):
            if grid[x][y].isdigit():
                if not pos:
                    pos = check_adjacency(x, y, grid)
                number += grid[x][y]
            else:
                if number != '' and pos:
                    numbers.append(int(number))
                    if pos not in gear_adjacents:
                        gear_adjacents[pos] = []
                    gear_adjacents[pos].append(int(number))
                # reset
                number = ''
                pos = None

    return numbers, gear_adjacents


def check_adjacency(x, y, grid):
    # all directions in the following order: NW,N,NE,E,SE,S,SW,W
    directions = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1),
                  (x, y - 1)]
    for x, y in directions:
        if 0 <= x < len(grid) and 0 <= y < len(grid[x]):
            if grid[x][y] not in '.\n' and not grid[x][y].isdigit():
                # found a symbol
                return x, y
    return None
