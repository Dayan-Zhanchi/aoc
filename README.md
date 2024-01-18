# Advent of code 2023
My solutions to aoc23. Code quality is non-existent here, I'm just trying to solve the problem with the approaches I come up with, mostly brute-force and or naive. I call it naive because most part 2 can't be solved with brute force, but most of them also don't require sophisticated algortihms to solve. I do minimal OO to avoid the boilerplates and I code mostly in imperative style, as that's what I'm used to.
For more elaborate thoughts and high-level explanations of my solutions you can find it in [days](days) folder. For a dumb aoc folder, I'm being overly verbose with explaining things and providing instructions here, but it's mostly for myself in case I ever go back to it.

## Input data
Note that the input folder is not included, as it seems to not be allowed according to aoc [policy](https://adventofcode.com/2023/about). So you will have to add it yourself in the root project as a folder named input.
Files added in the input folder should be named as `day<day_number>.txt` and `day<day_number>sample.txt` for the original input and sample input respectively. Note that if you are running the scraper, then the original input will be automatically added to the input folder along with the input folder if it doesn't exist. Currently, the sample input is not downloaded automatically and have to be added manually.
Also, if samples differ for part 1 vs part 2, then include them as `day<day_number>sample1.txt` and `day<day_number>sample2.txt` respectively in the input folder and when running the script include -s and -ds flag. 

To download the input files automatically from aoc, you need to include a scraping.ini file in the root folder of this project. The format should be:
```
[MAIN]
BaseUrl=https://adventofcode.com/2023/day
Delay=1
Retries=5
Scrape=True

[SESSION]
CookieSessionAOC=<Your-session-cookie>
```

## Some exceptions
**Input**
* Day 8 needs to be run with -ds flag along with -s if you want to run the samples, as there are designated samples for each part
* Day 20 part 2 only works with the original input, while part1 works for sample and original input. It's mostly because of how part 2 was meant to be solved.
* Day 24 part 1 lower and upper limit in p1 method has to be toggled depending on whether sample is running or original input. 

**Running time**

As I mostly use brute-force and or naive approach, the running times of some problems, especially towards the end of aoc are slow.
* Day 6 $\approx 6s$
* Day 10 $\approx 1m$
* Day 12 $\approx 5s$
* Day 17 $\approx 3s$ part 1 and $\approx 8s$ part 2
* Day 21 $\approx 2m40s$ part 2
* Day 22 $\approx 40s$ part 2
* Day 23 $\approx 50s$


## How to run
Run pip install like so `pip install -r requirements.txt`.

Run main.py with the correct year, day and whether you want to use sample + original input `py main.py -y 2023 -d 5 -s -o` and something like this will print out:
 ```
 day 5
 input type: sample, part: p1, solution: 35, time: 0.00000 ms
 input type: sample, part: p2, solution: 46, time: 0.00000 ms
 input type: original, part: p1, solution: 551761867, time: 0.99993 ms
 input type: original, part: p2, solution: 57451709, time: 1.00088 ms
 ```

## Flags
```
-y             # year of aoc
-d             # day of aoc problem
-s             # sample input, set to True if included, meaning to run sample input
-o             # original input, set to True if included, meaning to run original input
-ds            # different samples, set to True if included, meaning to run different samples for part 1 and 2
```
