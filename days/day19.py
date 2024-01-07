import operator
import re
from copy import deepcopy
import math

"""Similar to day 5 part 2, work with intervals + rule of product + watch out for off-by-one errors
Also, funny note, but the regex wasn't meant to work for workflow name e.g "in", only for the workflow entries, but it
worked, so I just extracted the correct position and called it a day for the input extraction.
"""


class Rule:
    val: int
    category: str
    op: operator  # operator op(a,b) means a op b, e.g a < b

    def __init__(self, val, category, op):
        self.val = val
        self.category = category
        self.op = op

    def __str__(self):
        return f"val: {self.val}, category: {self.category}, op: {self.op}"


class WorkFlowEntry:
    rule: Rule
    destination: str

    def __init__(self, rule, dest):
        self.rule = rule
        self.destination = dest

    def check_rule(self, categories):
        if self.rule:
            if self.rule.op(categories[self.rule.category], self.rule.val):
                return self.destination
            else:
                return False
        return self.destination

    def __str__(self):
        return f"rule: {self.rule}, destination: {self.destination}"


def parse(f):
    workflows_data, parts_data = [d.split('\n') for d in f.read().strip().split('\n\n')]
    workflows = {}  # {workflow_name: [workflow_entry]}
    for w in workflows_data:
        matches = re.findall(r'((\w)(<|>)(\d+):)?(\w+),?', w)
        workflow_name, final_dest = matches[0][-1], matches[-1][-1]
        workflows[workflow_name] = []
        if len(matches) > 2:
            for i in range(1, len(matches) - 1):
                m = matches[i]
                category, op, val, dest = m[1], m[2], m[3], m[4]
                op = operator.lt if op == "<" else operator.gt
                workflows[workflow_name].append(WorkFlowEntry(Rule(int(val), category, op), dest))
        workflows[workflow_name].append(WorkFlowEntry(None, final_dest))  # last always accepted so has no rule

    # {x: int, m: int, a: int, s: int}
    parts = [{e[0]: int(e[1]) for xmas in re.findall(r'\w=\d+', p) if (e := xmas.split('='))} for p in parts_data]
    return workflows, parts


def p1(f):
    workflows, parts = parse(f)
    accepted = []
    for p in parts:
        curr_workflow_name = 'in'
        while curr_workflow_name != 'A' and curr_workflow_name != 'R':
            for entry in workflows[curr_workflow_name]:
                destination = entry.check_rule(p)
                if destination:
                    break
            curr_workflow_name = destination
        if curr_workflow_name == 'A':
            accepted.append(p)

    return sum([v for a in accepted for _, v in a.items()])


def p2(f):
    workflows, _ = parse(f)
    accepted_states = []
    get_all_accepted(workflows, 'in', [], accepted_states)

    total_combinations = 0
    for accept in accepted_states:
        part_combination = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
        for entry in accept:
            if entry.rule:
                curr_interval = part_combination[entry.rule.category]
                match entry.rule.op:
                    case operator.lt:
                        if entry.rule.val < curr_interval[1]:
                            part_combination[entry.rule.category] = [curr_interval[0], entry.rule.val - 1]
                    case operator.gt:
                        if entry.rule.val > curr_interval[0]:
                            part_combination[entry.rule.category] = [entry.rule.val + 1, curr_interval[1]]
        total_combinations += math.prod([(v[1] - v[0]) + 1 for _, v in part_combination.items()])

    return total_combinations


def get_all_accepted(workflows, curr_workflow, curr_path, accepted_states):
    if curr_workflow == 'A':
        return tuple(curr_path)
    elif curr_workflow == 'R':
        return None

    c = deepcopy(curr_path)
    for idx, entry in enumerate(workflows[curr_workflow]):
        # because original workflow entry don't have the negative counterparts, have to add it manually,
        # e.g s < 1351 becomes s > 1350
        if idx + 1 > 1:
            prev_entry = workflows[curr_workflow][idx - 1]
            negated_op = operator.lt if prev_entry.rule.op == operator.gt else operator.gt
            negated_val = prev_entry.rule.val + 1 if prev_entry.rule.op == operator.gt else prev_entry.rule.val - 1
            c.append(WorkFlowEntry(Rule(negated_val, prev_entry.rule.category, negated_op), ''))

        candidate = deepcopy(c)
        candidate.append(entry)

        path = get_all_accepted(workflows, entry.destination, candidate, accepted_states)
        if path:
            accepted_states.append(path)
