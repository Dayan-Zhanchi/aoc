import re
import math
from dataclasses import dataclass

"""Cancer solution, but worked with intervals as tuples instead of ranges (as lists) as the latter sounded infeasible 
in python given the input, so had to watch out for alot of off-by-one error mistakes. The approach I went with was to 
apply the intervals in the form (start, range) to each mapping in the same way as in p1, but now instead I had to 
make sure that everytime an interval overlapped with a given entry in the map, a new interval was created (for the 
next mapping) according to the rules in p1 (but adapted to an interval). If the interval only partially overlapped, 
then the other part was sliced and iterated through to make a new interval for the next mapping. To not have to make 
two sliced intervals I sorted the map entries according to source, so there could only ever be one sliced interval 
each iteration (easier to see why by drawing examples), under assumption that there aren't any holes between the 
sources (which seemed to be the case when I checked)"""


@dataclass
class MapEntry:
    destination: int
    source_start: int
    range_length: int
    source_end: int


class Map:
    entries: [MapEntry]

    def __init__(self):
        self.entries = []


def parse(f):
    data = f.read().split('\n\n')
    data[-1] = data[-1][:-1]
    seeds = list(map(int, re.findall(r'\d+', data[0].split(':')[1])))
    maps = []
    for mapping in data[1:]:
        m = Map()
        for entry in mapping.split('\n')[1:]:
            entry_data = list(map(int, re.findall(r'\d+', entry)))
            source_end = entry_data[1] + entry_data[2] - 1
            m.entries.append(MapEntry(entry_data[0], entry_data[1], entry_data[2], source_end))
        m.entries = sorted(m.entries, key=lambda x: x.source_start)
        maps.append(m)

    return seeds, maps


def p1(f):
    seeds, maps = parse(f)
    nearest_location = math.inf
    for s in seeds:
        nearest_location = min(nearest_location, get_location(maps, s))

    return nearest_location


# runs in 0.9999275207519531ms ≈ 1ms
def p2(f):
    seeds, maps = parse(f)
    seeds = [(seeds[idx], seeds[idx + 1]) for idx in range(0, len(seeds), 2) if idx < len(seeds)]  # (start, range)

    intervals = seeds
    for curr_map in maps:
        new_intervals = []
        for curr_interval in intervals:
            for entry in curr_map.entries:
                # assuming a given map doesn't have holes
                curr_start = curr_interval[0]
                if entry.source_start <= curr_start <= entry.source_end:
                    sub_interval, curr_interval = get_sub_interval(entry, curr_interval)
                    new_intervals.append(sub_interval)
                else:
                    continue

                if curr_interval is None:
                    # break early because if no slices then it can't possibly overlap with the upcoming entries,
                    # since the entries are sorted
                    break

            if curr_interval is not None:
                new_intervals.append(curr_interval)

        intervals = new_intervals

    # suffices to only look at start point of each interval and pick the minimum
    return sorted(intervals, key=lambda x: x[0])[0][0]


def get_location(maps, seed):
    current_location = seed
    for curr_map in maps:
        for entry in curr_map.entries:
            if entry.source_start <= current_location <= entry.source_end:
                current_location = entry.destination + abs(current_location - entry.source_start)
                break

    return current_location


def get_sub_interval(entry, curr_interval):
    curr_start = curr_interval[0]
    curr_range = curr_interval[1]
    curr_end = curr_start + curr_range - 1
    source_offset = abs(curr_start - entry.source_start)
    new_interval_start = entry.destination + source_offset
    if curr_end <= entry.source_end:
        new_interval_end = curr_range
        rest_interval = None
    else:
        new_interval_end = (entry.source_end - curr_start) + 1
        rest_interval = (entry.source_end + 1, curr_range - new_interval_end)

    return (new_interval_start, new_interval_end), rest_interval
