import re

"""
another method is simply to use .index to get the first occurence of the digit and reverse the text
and use .index again to get the last occurence of the digit, after converting word to ints or ints to words,
so they have the same format
"""


def parse(f):
    return f.readlines()


def p1(f):
    data = parse(f)
    total = 0
    for text in data:
        numbers = re.findall(r'\d', text)
        number_to_add = int("".join(numbers[0] + numbers[-1])) if len(numbers) > 1 else int(numbers[0] + numbers[0])
        total += number_to_add

    return total


def p2(f):
    data = parse(f)
    pattern2 = r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))'  # positive lookahead ?= to catch the overlaps
    total = 0
    for text in data:
        numbers = re.findall(pattern2, text)
        nr1 = str2int(numbers[0])
        nr2 = nr1
        if len(numbers) > 1:
            nr2 = str2int(numbers[-1])
        total += 10 * nr1 + nr2

    return total


def str2int(text):
    words2numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                     "eight": 8, "nine": 9}
    if text.isdigit():
        return int(text)
    return words2numbers[text]
