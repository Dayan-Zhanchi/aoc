import re
import math

"""Was thinking of some contrived algorithm to do part2, where I try to remember the paths from a start node to a 
node ending with 'Z' by storing tuples in the form (start point, directions to reach the node ending with z from the 
start node) as keys and val as steps to reach the node (e.g 'LLLRLL'). That way I could increment the 
steps (jumping ahead) once I knew I had already walked that path. In worst case this would blow up the memory and it 
would work poorly if one node visited a node ending with 'Z' at the end, or if the steps were just too low to make an 
impact. So I had to verify if this was feasible by checking when the each node first visited a node ending with 'Z', 
which turned out to be a constant cyclic number for each node (each node with it's own constant cyclic number).
Knowing this I realized that I could simply use lcm to calculate the answer."""

direction = {'L': 0, 'R': 1}


def parse(f):
    instruction, nodes = f.read().split('\n\n')
    nodes = nodes.split('\n')
    network = {match.group(1): (match.group(2), match.group(3)) for text in nodes
               if (match := re.match(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', text))}
    return instruction, network


def p1(f):
    instructions, network = parse(f)

    steps = 0
    current_node = 'AAA'
    while True:
        for i in instructions:
            if current_node in network:
                current_node = network[current_node][direction[i]]
            steps += 1

            if current_node == 'ZZZ':
                return steps


def p2(f):
    instructions, network = parse(f)

    steps = 0
    current_nodes = [node for node in network if node[-1] == 'A']
    steps_found_z = []
    found = [False] * len(current_nodes)
    all_found = False
    while not all_found:
        for i in instructions:
            tmp_nodes = []
            steps += 1
            for idx, node in enumerate(current_nodes):
                n = network[node][direction[i]]
                if n[-1] == 'Z' and not found[idx]:
                    found[idx] = True
                    steps_found_z.append(steps)

                tmp_nodes.append(n)

            if all(found):
                all_found = True
                break

            current_nodes = tmp_nodes

    return math.lcm(*steps_found_z)
