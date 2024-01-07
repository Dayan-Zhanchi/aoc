import get_input
from importlib import import_module, reload
import os
from time import time
from configparser import ConfigParser
import argparse


def run(module, input_type, file_name):
    for i in ["p1", "p2"]:
        if not hasattr(module, i):
            continue
        with open(file_name, 'r') as f:
            func = getattr(module, i)
            start = time()
            solution = func(f)
            printer(i, input_type, solution, time() - start)


def printer(part, input_type, solution, time):
    print(f"input type: {input_type}, part: {part}, solution: {solution}, time: {time_conversion(time)}")


def time_conversion(time):
    ms1, mus = divmod(time * 1e6, 1e3)
    ss1, ms = divmod(time * 1e3, 1e3)
    mm, ss = divmod(time, 60)
    hh, mm = divmod(mm, 60)
    if hh > 0:
        return f"{hh}h:{mm}m:{ss}s"
    elif mm > 0:
        return f"{mm}m:{ss}s"
    elif ss1 > 0:
        return f"{time:.2f}s"
    elif ms1 > 0:
        return f"{time * 1e3:.2f}ms"
    else:
        return f"{time * 1e6:.2f}μs"


def main():
    parser = argparse.ArgumentParser(description="Aoc23")
    parser.add_argument('--year', '-y', type=int, default=2023, help='Year to run')
    parser.add_argument('--day', '-d', type=int, default=19, help='Year to run')
    parser.add_argument('--input_type', '-i', action=argparse.BooleanOptionalAction,
                        help='To run only sample or both sample and original')
    args = parser.parse_args()
    config = ConfigParser()
    config.read('scraping.ini')

    to_scrape = config.getboolean('MAIN', 'Scrape')
    input_dir = "input"
    day = args.day
    year = args.year
    original = args.input_type
    file_name = os.path.join(input_dir, f"day{day}.txt")
    file_name_sample = os.path.join(input_dir, f"day{day}sample.txt")

    # only downloads once and then caches the downloaded file in the input folder of the root project
    if to_scrape:
        get_input.download_input(day, file_name, input_dir)
        get_input.download_sample_input(day, file_name_sample, input_dir)

    # dynamically import a file and run it
    module_name = f"days.day{day}"
    module = import_module(module_name)
    print(f"day {day}")
    run(module, "sample", file_name_sample)
    if original:
        reload(module)
        run(module, "original", file_name)


if __name__ == "__main__":
    main()

# TODO: run all days option or run a subset of days
# TODO: time also includes time for parsing
