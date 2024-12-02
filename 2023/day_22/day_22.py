import numpy as np


def read_input(fname):
    bricks = np.zeros((300, 10, 10), dtype="int")
    brick_map = {}
    support_map = {}
    with open(fname) as file:
        i = 1
        for line in file.readlines():
            a, b = line.strip().split("~")
            a = [int(x) for x in a.split(",")]
            b = [int(x)+1 for x in b.split(",")]
            bricks[a[2]:b[2], a[0]:b[0], a[1]:b[1]] = i
            brick_map[i] = {"stationary": False,
                            "support": False}
            support_map[i] = set()
            i += 1
    return bricks, brick_map, support_map


def get_min_z(brick, bricks):
    return np.where(bricks == brick)[0].min()


def sort_bricks(bricks, brick_map):
    b = list(np.unique(bricks))
    b.remove(0)
    result = [(get_min_z(brick, bricks), brick) for brick in b
              if not brick_map[brick]["stationary"]]
    sorted_z, sorted_b = zip(*sorted(result))
    return sorted_z, sorted_b


def get_block_below(brick, bricks):
    brick_grid = np.where(bricks == brick)
    z = brick_grid[0]
    z_below = z - 1
    below = bricks[(z_below, brick_grid[1], brick_grid[2])]
    blocks_below = set(np.unique(below))
    blocks_below.discard(brick)
    blocks_below.discard(0)
    return blocks_below


def drop_brick(brick, bricks):
    brick_grid = np.where(bricks == brick)
    z = brick_grid[0]
    z_below = z - 1
    bricks[brick_grid] = 0
    bricks[(z_below, brick_grid[1], brick_grid[2])] = brick
    return bricks


def part_1(bricks, brick_map, support_map):
    _, sorted_bricks = sort_bricks(bricks, brick_map)
    while not all([b["stationary"] for b in brick_map.values()]):
        # drop all non-stationary bricks
        pairs = [(get_min_z(b, bricks), b) for b in sorted_bricks
                 if not brick_map[b]["stationary"]]
        for z, b in pairs:
            bricks = drop_brick(b, bricks)
            # make stationary if at bottom
            if z - 1 == 0:
                brick_map[b]["stationary"] = True
            # stationary if bricks under it
            else:
                blocks_below = get_block_below(b, bricks)
                blocks_below = {b for b in blocks_below if brick_map[b]["stationary"]}
                if blocks_below:
                    brick_map[b]["stationary"] = True
                    support_map[b] |= blocks_below
    num_blocks = len(support_map)
    critical_blocks = set()
    for s_blocks in support_map.values():
        if len(s_blocks) == 1:
            critical_blocks |= s_blocks
    n_critical = len(critical_blocks)
    print(f"\tNumber of blocks: {num_blocks}, Number critical: {n_critical}")
    return num_blocks - n_critical


def chain_reaction(bottom_brick, blocks_supporting, supported_by, removed):
    fallen = set()
    removed.add(bottom_brick)
    for top_brick in supported_by[bottom_brick]:
        supporting_bricks = blocks_supporting[top_brick]
        if not supporting_bricks.difference(removed):
            fallen.add(top_brick)
            fallen |= chain_reaction(top_brick, blocks_supporting, supported_by, removed)
    return fallen


def part_2(bricks, brick_map, blocks_supporting):
    _, sorted_bricks = sort_bricks(bricks, brick_map)
    supported_by = {b: set() for b in sorted_bricks}
    while not all([b["stationary"] for b in brick_map.values()]):
        # drop all non-stationary bricks
        pairs = [(get_min_z(b, bricks), b) for b in sorted_bricks
                 if not brick_map[b]["stationary"]]
        for z, b in pairs:
            bricks = drop_brick(b, bricks)
            # make stationary if at bottom
            if z - 1 == 0:
                brick_map[b]["stationary"] = True
            # stationary if bricks under it
            else:
                blocks_below = get_block_below(b, bricks)
                blocks_below = {b for b in blocks_below if brick_map[b]["stationary"]}
                if blocks_below:
                    brick_map[b]["stationary"] = True
                    blocks_supporting[b] |= blocks_below
                    for bb in blocks_below:
                        supported_by[bb].add(b)
    chain_reaction_value = {}
    for b in supported_by:
        chain_reaction_value[b] = len(
            chain_reaction(b, blocks_supporting, supported_by, set())
        )
    return sum(chain_reaction_value.values())


if __name__ == "__main__":
    print("Part 1 test 1:", part_1(*read_input("test.txt")))
    print("Part 1:", part_1(*read_input("input.txt")))
    print("Part 2 test 1:", part_2(*read_input("test.txt")))
    print("Part 2:", part_2(*read_input("input.txt")))
