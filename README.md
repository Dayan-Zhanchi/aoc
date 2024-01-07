# Advent of code 2023
My solutions to aoc23. Code quality is non-existent here, I'm just trying to solve the problem with the approaches I come up with, mostly brute-force. I do minimal OO to avoid the boilerplates. I code mostly in imperative style, as that's what I'm used to.
For more elaborate thoughts and high-level explanations of my solutions you can find it in [days](days) folder. For a dumb aoc folder, I'm being overly verbose with explaining things and providing instructions here, but oh well, better be proper in case someone ever wants to run the code.

# Input data
Note that the input folder is not included, as it seems to not be allowed according to aoc [policy](https://adventofcode.com/2023/about). So you will have to add it yourself in the root project as a folder named input.
Files added in the input folder should be named as `day<day_number>.txt` and `day<day_number>sample.txt` for the original input and sample input respectively. Note that if you are running the scraper, then the original input will be automatically added to the input folder along with the input folder if it doesn't exist. Currently, the sample input is not downloaded automatically and have to be added manually.

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

# How to run
Run pip install like so `pip install -r requirements.txt`.

Run main.py with the correct year, day and whether you want to use sample + original input `py main.py -y 2023 -d 5 -i` and something like this will print out:
 ```
 day 5
 input type: sample, part: p1, solution: 35, time: 0.00000 ms
 input type: sample, part: p2, solution: 46, time: 0.00000 ms
 input type: original, part: p1, solution: 551761867, time: 0.99993 ms
 input type: original, part: p2, solution: 57451709, time: 1.00088 ms
 ```

# Flags
```
--y             # year of aoc
--d             # day of aoc problem
--i             # input type, set to True if included, meaning to run both sample + original input, otherwise if not included only sample input
```
