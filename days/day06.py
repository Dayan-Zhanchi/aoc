import re
import math

"""
Brute force just as good, as input isn't too large (less than 100mil). In hindsight could have used quadratic 
formula as the condition is (time - x)x > d <=> (time - x)x - d > 0 and solve for as if they are equal. That
gives the range between acceptable solutions. 
"""


def parse(f):
    data = f.readlines()
    times = list(map(int, re.findall(r'\d+', data[0].split(':')[1])))
    distances = list(map(int, re.findall(r'\d+', data[1].split(':')[1])))
    return times, distances


def p1(f):
    times, distances = parse(f)
    # formula is (time - x) * x = traveled distance, where x is the time the button is held
    candidates = get_candidates(distances, times)

    return math.prod(candidates)


def p2(f):
    data = parse(f)
    big_time = [int(''.join(map(str, data[0])))]
    big_distance = [int(''.join(map(str, data[1])))]

    return get_candidates(big_distance, big_time)[0]


def get_candidates(distances, times):
    candidates = list(
        map(len, [[trav_dist for t in range(1, time) if (trav_dist := traveled_dist(time, t)) > distances[idx]]
                  for idx, time in enumerate(times)]))
    return candidates


def traveled_dist(time, x):
    return (time - x) * x
