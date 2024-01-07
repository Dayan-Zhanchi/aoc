import re

"""not much to say, straightforward brute-force implementation
in hindsight could have reversed the sequences for the second part (although I did reverse it at some point, but only to avoid going backwards in the loop...) . 
Also one liners functional style would be more readable for this problem or use recursion."""


def parse(f):
    return [list(map(int, sequence)) for sequence in [re.findall(r'-?\d+', d) for d in f.readlines()]]


def p1(f):
    data = parse(f)
    return sum(get_extrapolated_vals(data, -1))


def p2(f):
    data = parse(f)
    return sum(get_extrapolated_vals(data, 0))


def get_extrapolated_vals(data, extrapolate_orientation):
    extrapolated_vals = []
    for seq in data:
        diff_seq = [seq]
        end = False
        count = 0
        while not end:
            tmp = []
            for pair in zip(diff_seq[count], diff_seq[count][1:]):
                tmp.append(pair[1] - pair[0])

            diff_seq.append(tmp)
            count += 1

            if len(tmp) == 1 or tmp == ([0] * len(tmp)):
                end = True

        diff_seq = list(reversed(diff_seq))
        for i in range(0, len(diff_seq) - 1):
            if extrapolate_orientation == -1:
                diff_seq[i + 1].append(diff_seq[i + 1][-1] + diff_seq[i][-1])
            else:
                diff_seq[i + 1].insert(extrapolate_orientation,
                                       diff_seq[i + 1][extrapolate_orientation] - diff_seq[i][extrapolate_orientation])

        if extrapolate_orientation == -1:
            extrapolated_vals.append(diff_seq[-1][-1])
        else:
            extrapolated_vals.insert(extrapolate_orientation, diff_seq[-1][extrapolate_orientation])

    return extrapolated_vals
