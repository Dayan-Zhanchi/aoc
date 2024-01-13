import numpy as np
from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class SandBrick:
    id: int
    x: tuple
    y: tuple
    z: tuple
    supported_by: list = field(default_factory=list)


def parse(f):
    # max z = 307 (checked the input), x,y = 9,9
    # min z = 1 and x,y = 0,0
    id = 1
    sand_bricks_fast_lookup = {}  # {id: SandBrick}
    sand_bricks_snapshot = []
    grid = np.zeros((10, 10, 310)).astype(int)  # 3D grid to keep track of sand brick positions
    for data in f.read().splitlines():
        coord1, coord2 = data.split('~')
        coord1 = list(map(int, coord1.split(',')))
        coord2 = list(map(int, coord2.split(',')))
        sand_brick = SandBrick(id, (coord1[0], coord2[0]), (coord1[1], coord2[1]), (coord1[2], coord2[2]))
        sand_bricks_snapshot.append(sand_brick)
        sand_bricks_fast_lookup[id] = sand_brick
        grid[*get_index_coord(sand_brick.x, sand_brick.y, sand_brick.z)] = sand_brick.id
        id += 1

    sand_bricks_snapshot = list(sorted(sand_bricks_snapshot, key=lambda brick: brick.z[0]))
    return grid, sand_bricks_snapshot, sand_bricks_fast_lookup


def p1(f):
    grid, sand_bricks_snapshot, sand_bricks_fast_lookup = parse(f)
    grid_settled, _ = settle_bricks(deepcopy(grid), sand_bricks_snapshot)
    return calculate_disintegratables(grid_settled, sand_bricks_snapshot, sand_bricks_fast_lookup)


# slow 40s
def p2(f):
    grid, sand_bricks_snapshot, sand_bricks_fast_lookup = parse(f)
    grid_settled, _ = settle_bricks(deepcopy(grid), sand_bricks_snapshot)
    sand_bricks_settled = list(sorted(sand_bricks_snapshot, key=lambda brick: brick.z[0]))
    number_of_falling_bricks = 0
    for brick in sand_bricks_settled:
        ids = get_ids(grid_settled, brick.x, brick.y, (brick.z[1] + 1, brick.z[1] + 1))
        if len(ids) == 0:
            continue
        else:
            # small optimization, but not really needed, if blocks above don't fall then there won't be any chain reaction
            if all([len(sand_bricks_fast_lookup[i].supported_by) > 1 for i in ids]):
                continue

            # remove one brick and let bricks settle again, count the number of bricks that settled
            test_grid = deepcopy(grid_settled)
            test_sand_bricks = deepcopy(sand_bricks_settled)
            test_grid[*get_index_coord(brick.x, brick.y, brick.z)] = 0
            test_sand_bricks.remove(brick)
            _, falling_bricks = settle_bricks(test_grid, test_sand_bricks)
            number_of_falling_bricks += falling_bricks

    return number_of_falling_bricks


def calculate_disintegratables(grid_settled, sand_bricks_settled, sand_bricks_fast_lookup):
    disintegrated = 0
    legit_bricks = []
    for brick in sand_bricks_settled:
        # always check directly above
        z = brick.z
        # don't care about getting entire range of z vertical, just need to know the sand cube directly above it on the z-axis
        # so for vertical only the very end is relevant, but for non-vertical the start and end is the same
        ids = get_ids(grid_settled, brick.x, brick.y, (z[1] + 1, z[1] + 1))
        if len(ids) == 0:
            disintegrated += 1
            legit_bricks.append(brick.id)
        else:
            if all([len(sand_bricks_fast_lookup[i].supported_by) > 1 for i in ids]):
                disintegrated += 1
                legit_bricks.append(brick.id)

    return disintegrated


def settle_bricks(grid, sand_bricks_falling):
    bricks_that_fell = 0
    for brick in sand_bricks_falling:
        if brick.z[0] == 1:
            continue

        # let the brick fall
        x, y, z = brick.x, brick.y, brick.z
        while z[0] > 1:
            ids = get_ids(grid, brick.x, brick.y, (z[0] - 1, z[0] - 1))
            if any(ids):
                # add the non-zero ids, constituting supporting blocks
                brick.supported_by = [*brick.supported_by, *ids[ids != 0]]
                break
            z = (z[0] - 1, z[1] - 1)

        if brick.z != z:
            bricks_that_fell += 1

        grid[*get_index_coord(brick.x, brick.y, brick.z)] = 0  # remove the brick from its original pos
        grid[*get_index_coord(x, y, z)] = brick.id  # populate the new positions with brick id
        # set brick to its new pos
        brick.x = (x[0], x[1])
        brick.y = (y[0], y[1])
        brick.z = (z[0], z[1])

    return grid, bricks_that_fell


def get_index_coord(x, y, z):
    coord = []
    for v in [x, y, z]:
        if v[0] == v[1]:
            coord.append(v[0])
        else:
            coord.append(range(v[0], v[1] + 1))
    return coord


def get_ids(grid, x, y, z):
    bricks = grid[*get_index_coord(x, y, z)]
    bricks = bricks if isinstance(bricks, np.ndarray) else np.array([bricks])
    return np.array(list(set(bricks[bricks != 0])))  # remove duplicated ids, because bricks can extend
