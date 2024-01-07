from functools import reduce
import re

"""One of the easier puzzles overall, but unecessarily wordy (undestanding the problem was harder than implementing it),
could have been day 1-3. All the instructions and edge cases where already given in the puzzle, so it was just a 
straightforward implementation"""

MULTIPLIER = 17
MOD = 256


def parse(f):
    return f.read().replace('\n', '').split(',')


def p1(f):
    data = parse(f)
    return sum([special_hash(instruction) for instruction in data])


def p2(f):
    data = parse(f)
    boxes = {}
    for d in data:
        label, operation, focal_length = extract_instruction(d)
        box_number = special_hash(label)
        if box_number not in boxes:
            boxes[box_number] = []

        box_to_alter = [(idx, b) for idx, b in enumerate(boxes[box_number]) if b[0] == label]
        if operation == '-':
            if box_to_alter:
                boxes[box_number].remove(box_to_alter[0][1])
        else:
            if box_to_alter:
                boxes[box_number][box_to_alter[0][0]] = (label, int(focal_length))
            else:
                boxes[box_number].append((label, int(focal_length)))

    return calc_focusing_power(boxes)


def special_hash(instruction):
    return reduce(lambda acc, a: ((ord(a) + acc) * MULTIPLIER) % MOD, instruction, 0)


def extract_instruction(instruction):
    return re.findall(r'([a-z]+)(=|-)(\d+)?', instruction)[0]


def calc_focusing_power(boxes):
    return sum([(key + 1) * (idx + 1) * b[1] for key, box in boxes.items() for idx, b in enumerate(box)])
