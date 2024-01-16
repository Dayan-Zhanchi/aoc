from dataclasses import dataclass, field
import re
from enum import Enum, auto
from collections import defaultdict
import math

# part 1 straightforward OO implementation and part 2 similar to day 8


class PulseType(Enum):
    LOW = auto()
    HIGH = auto()


class ModuleType(Enum):
    FLIPFLOP = auto()
    CONJUNCTION = auto()
    BROADCAST = auto()


@dataclass
class Pulse:
    sender: str
    receiver: str
    type: PulseType


@dataclass
class Module:
    id: str
    type: ModuleType
    connections: [str]


@dataclass
class FlipFlopModule(Module):
    on: bool = field(default=False, kw_only=True)

    def out(self, pulse):
        output = []
        if pulse.type is PulseType.LOW:
            output = [Pulse(self.id, d, PulseType.LOW) if self.on else Pulse(self.id, d, PulseType.HIGH)
                      for d in self.connections]
            self.on = not self.on
        return output


@dataclass
class ConjunctionModule(Module):
    prev_pulses: dict[str, PulseType] = field(default_factory=dict, kw_only=True)

    def out(self, pulse):
        self.prev_pulses[pulse.sender] = pulse.type
        pulse_to_send = PulseType.LOW if self.__check_all_high_pulses() else PulseType.HIGH
        return [Pulse(self.id, d, pulse_to_send) for d in self.connections]

    def __check_all_high_pulses(self):
        return all([pulse == PulseType.HIGH for _, pulse in self.prev_pulses.items()])


@dataclass
class BroadcastModule(Module):
    def out(self):
        return [Pulse(self.id, d, PulseType.LOW) for d in self.connections]


def parse(f):
    data = f.read().splitlines()
    mother_module = {}
    connected_by = defaultdict(lambda: set())
    for d in data:
        prefix, module_id, connections = extract_modules_and_connections(d)
        match prefix:
            case '%':
                mother_module[module_id] = FlipFlopModule(module_id, ModuleType.FLIPFLOP, connections)
            case '&':
                mother_module[module_id] = ConjunctionModule(module_id, ModuleType.CONJUNCTION, connections)
            case _:
                mother_module[module_id] = BroadcastModule(module_id, ModuleType.BROADCAST, connections)

        for c in connections:
            connected_by[c].add(module_id)

    # populate conjunction module most recent pulses with low
    for d in filter(lambda x: x[0] == '&', data):
        prefix, module_id, _ = extract_modules_and_connections(d)
        for c in connected_by[module_id]:
            mother_module[module_id].prev_pulses[c] = PulseType.LOW

    return mother_module


def extract_modules_and_connections(d):
    module, connections = d.split('->')
    match = re.match(r'(%|&)?(\w+)', module)
    prefix, module_id = match[1], match[2]
    connections = re.findall(r'\w+', connections)
    return prefix, module_id, connections


def p1(f):
    mother_module = parse(f)
    broadcaster = mother_module['broadcaster']
    button_pushes = 1000
    counts = {PulseType.LOW: 0, PulseType.HIGH: 0}
    for _ in range(button_pushes):
        q = broadcaster.out()
        counts[PulseType.LOW] += 1
        # one full sequence from a button push ends when the queue is empty
        while q:
            curr_pulse = q.pop(0)
            counts[curr_pulse.type] += 1
            output = mother_module[curr_pulse.receiver].out(curr_pulse) \
                if curr_pulse.receiver in mother_module else None
            # when flip-flop receives a high pulse ignore it
            if not output:
                continue
            q = [*q, *output]
    return math.prod(val for _, val in counts.items())


def p2(f):
    mother_module = parse(f)
    broadcaster = mother_module['broadcaster']
    button_pushes = 0
    track_counts = {'gp': 0, 'ln': 0, 'xp': 0, 'xl': 0}
    while not all([v != 0 for _, v in track_counts.items()]):
        q = broadcaster.out()
        button_pushes += 1
        while q:
            curr_pulse = q.pop(0)
            output = mother_module[curr_pulse.receiver].out(curr_pulse) \
                if curr_pulse.receiver in mother_module else None
            if (output and curr_pulse.sender in track_counts and curr_pulse.receiver == 'df' and
                    curr_pulse.type == PulseType.HIGH and not track_counts[curr_pulse.sender]):
                track_counts[curr_pulse.sender] = button_pushes
            if not output:
                continue
            q = [*q, *output]

    return math.lcm(*[v for _, v in track_counts.items()])
