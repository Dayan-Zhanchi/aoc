import re
from math import prod
from dataclasses import dataclass

# in hindsight could have just used r'(\d+) (red|green|blue)'

p_red = r'(?P<r>\d+) red'
p_green = r'(?P<g>\d+) green'
p_blue = r'(?P<b>\d+) blue'
p_colors = [p_red, p_green, p_blue]


@dataclass
class Game:
    cube_sets: [tuple]


def parse(f):
    games = []
    data = f.readlines()
    for d in data:
        cube_sets_text = d.split(';')
        cube_sets = []
        for c in cube_sets_text:
            r, g, b = color_extract(c)
            cube_sets.append((r, g, b))
        games.append(Game(cube_sets))

    return games


def color_extract(text):
    capturing_group = ['r', 'g', 'b']
    return [int(m.group(capturing_group[idx])) if (m := re.search(pattern, text)) else 0
            for idx, pattern in enumerate(p_colors)]


def p1(f):
    data = parse(f)
    cube_set_limit = (12, 13, 14)
    total = 0
    for game_id, game in enumerate(data, 1):
        valid_cube_sets = []
        for cube_set in game.cube_sets:
            valid_cube_sets.append(all([a <= b for a, b in zip(cube_set, cube_set_limit)]))

        if all(valid_cube_sets):
            total += game_id

    return total


def p2(f):
    data = parse(f)
    return sum([prod([max(i) for i in zip(*game.cube_sets)]) for game in data])
